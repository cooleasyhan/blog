Date: 2016-08-12
Title: salt REQ 数据传输
Tags: Salt
sulg: salt_transport



## /u01/github/salt-develop/salt/transport/zeromq.py : class AsyncZeroMQReqChannel
这是ZEROMQ的一个底层封装程序,实现了单例模式,ZEROMQ REQ/REP 模式中的 REQ send 方法, REQ/REP 是一个低效的,类似于socket 的通讯模式, 发起一次REQ,等待一个REP,
不会进行多次消息交互,给salt用还是挺合理的,发送一个命令给minion, minion 返回一个执行结果。 原始的REQ/REP不支持异步,通过使用tornado实现异步操作。

### 单例:
首先是根据 io_loop, io_loop如果为空,则使用zmq自带的tornado, ioloop
```python
io_loop = kwargs.get('io_loop')
        if io_loop is None:
            zmq.eventloop.ioloop.install()
            io_loop = tornado.ioloop.IOLoop.current()
        if io_loop not in cls.instance_map:
            cls.instance_map[io_loop] = weakref.WeakValueDictionary()
        loop_instance_map = cls.instance_map[io_loop]
```

key:
```python
return (opts['pki_dir'],     # where the keys are stored
                opts['id'],          # minion ID
                kwargs.get('master_uri', opts.get('master_uri')),  # master ID
                kwargs.get('crypt', 'aes'),  # TODO: use the same channel for crypt
                )
```

核心对象:
```python
self.message_client = AsyncReqMessageClient(self.opts,
                                                    self.master_uri,
                                                    io_loop=self._io_loop,
                                                    )

```


核心方法(这里不考虑权限):
```python
    @tornado.gen.coroutine
    def _uncrypted_transfer(self, load, tries=3, timeout=60):
        '''
        Send a load across the wire in cleartext

        :param dict load: A load to send across the wire
        :param int tries: The number of times to make before failure
        :param int timeout: The number of seconds on a response before failing
        '''
        ret = yield self.message_client.send(
            self._package_load(load),
            timeout=timeout,
            tries=tries,
        )

        raise tornado.gen.Return(ret)
```


## /u01/github/salt-develop/salt/transport/zeromq.py : class AsyncReqMessageClient

_init_socket
```python
# 使用REQ
self.socket = self.context.socket(zmq.REQ)

# 启用异步
self.socket.connect(self.addr)
self.stream = zmq.eventloop.zmqstream.ZMQStream(self.socket, io_loop=self.io_loop)
```


```python
@tornado.gen.coroutine
def _internal_send_recv(self):
    while len(self.send_queue) > 0:
        message = self.send_queue[0]
        future = self.send_future_map.get(message, None)
        if future is None:
            # Timedout
            del self.send_queue[0]
            continue

        # 设置on_recv方法, 收到消息,调用 future.set_result
        # send
        def mark_future(msg):
            if not future.done():
                data = self.serial.loads(msg[0])
                future.set_result(data)
        self.stream.on_recv(mark_future)
        self.stream.send(message)

        # 返回future
        try:
            ret = yield future
        except:  # pylint: disable=W0702
            self._init_socket()  # re-init the zmq socket (no other way in zmq)
            del self.send_queue[0]
            continue
        del self.send_queue[0]
        self.send_future_map.pop(message, None)
        self.remove_message_timeout(message)
```

