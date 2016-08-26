Date: 2016-08-18
Title: tornado coroutine 协程源码分析
Tags: python
slug: tornado_coroutine


要想理解tornado coroutine, 就需要先了解什么是yield。下面做了一个简单介绍和demo。
yield 返回函数,但是记录函数上下文,等待调用next后接着执行。  使用yield的函数自动变成一个生成器。也就是可以通过 for i in xxx 执行。  

```python
def test():
    print 'enter'
    while 1:
        b = yield
        yield b



# f.next() 与 f.send(None) 等价。
f = test()
f.send(None) # f.next()
print f.send(1)
f.next()
print f.send(2)
f.next()
print f.send(3)
f.next()


#### rst:
enter
1
2
3

```

但要实现协程,仅仅依靠yield,或者说迭代器是不够的, 迭代器会将控制权返回上层调用者, 而协程必须能够知道什么时候能够接着往下执行。这就轮到 tornado 的 ioLoop 大显身手的时候了, 它是一个顶层的调度程序。他会负责在合适的时候接着往下执行。  
**整体来说, 我们通过ioloop这个顶层调度程序,控制着多个子例程,这些子例程会在运行长时间操作时,比如io操作等,通过yield返回。 而ioloop程序会在正确的时候重新启动这个例程。**

## DEMO代码
下面是一个简单的demo的全部代码, 这里主要有两个新对象,一个tornado.gen.coroutine 修饰符,和tornado.concurrent.Future 对象。
在一个常见的coroutine方法,一般只需下面三个步骤  

+ 获取IOLoop实例,这里使用了单利模式。
+ 我们会new一个Future对象, 利用ioloop的add_callback方法,为其增加一个callback方法,而这个callback方法会设置Future对象的结果,将Future标记为已完成。
+ start ioloop, ioloop 会循环调用callback方法, 并检测Future对象是否已经完成,如果完成则将控制权返回至相应协程。

### ioloop
```python
# 一般情况下,只有一个ioloop存在于应用的主线程中,使用instance获取。
ioloop = tornado.ioloop.IOLoop.instance()
# 而其他情况,可以通过current获取当前线程中的ioloop
ioloop = tornado.ioloop.IOLoop.current()
```
    

### code
```python
# coding=utf-8
import tornado.concurrent
import tornado.ioloop
from tornado.gen import coroutine, sleep


class Demo(object):
    def __init__(self, io_loop):
        self.io_loop = io_loop

    # 为简化源码分析,直接返回回结果
    def do_something_long(self, a, b):
        self._future.set_result(a + b)

    # @coroutine
    # def do_something_long(self, a, b):
    #     import random
    #     s = random.randint(5, 5)
    #     yield sleep(s)
    #     self._future.set_result(a + b)
    #
    
    @coroutine
    def asyn_sum(self, a, b):
        print " asyn_sum", a, b
        if hasattr(self, '_future') and not self._future.done():  
            future = self._future  
        else:
            future = tornado.concurrent.Future()
            self._future = future
            self.io_loop.add_callback(self.do_something_long, a=a, b=b)

        result = yield self._future

        print("after yielded")
        print a, b, result


def main():
    ioloop = tornado.ioloop.IOLoop.instance()

    t1 = Demo(ioloop)
    print t1.asyn_sum(2, 3)
    t2 = Demo(ioloop)
    print t2.asyn_sum(2, 3)

    print 'start ', '*' * 20
    ioloop.start()


if __name__ == "__main__":
    main()

```


## 源码分析

具体源码还请自行查看, 下面只是摘录了部分源码,下面代码也有部分注释。

整个流程大体是这样的, 我们自定义一个使用 @coroutine 修饰符的迭代器, 迭代器里定义一个future,通过yield返回。 @coroutine 修饰符会帮忙做第一次next执行,将得到的迭代器,组装一个Runner对象,
而Runner对象将设定自定义future的done_callback为Runner的run方法,run方法又会将结果send至自定义future,使其继续执行。  
这里需要注意的是coroutine也会实现一个Future, 但并未加入到io_loop的callback列表中,在我们的demo中,也并没有进一步使用。 


**一句话就是,我们定义一个function,yield 一个future,给其添加一个callback,设置future的result, 而coroutine帮我们添加了一个callback,在future完成时,能够接着执行我们的funciton,
总共2个callback搞定**

### coroutine
```python

def _make_coroutine_wrapper(func, replace_callback):
    
    ...

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        future = TracebackFuture()

        ...

        try:
            执行带yield语句的function,会返回一个迭代器
            result = func(*args, **kwargs)
        except (Return, StopIteration) as e:
            result = _value_from_stopiteration(e)
        except Exception:
            future.set_exc_info(sys.exc_info())
            return future
        else:
            if isinstance(result, GeneratorType):
                # 是迭代器,并进行第一次执行
                try:
                    ...
                    yielded = next(result) # 这里yielded 也是一个future对象,由我们asyn_sum方法yield返回
                    ...
                except (StopIteration, Return) as e:
                    future.set_result(_value_from_stopiteration(e))
                except Exception:
                    future.set_exc_info(sys.exc_info())
                else:
                    Runner(result, future, yielded) 
                    # 将迭代器:result, coroutine的future, 自定义方法的future 组装,
                    # 当自定义的future设置了result后会执行其run方法
                try:
                    return future
                finally:
                    future = None
        # 如果不是迭代器,则直接将设置result并返回
        future.set_result(result)
        return future
    return wrapper

```


### Runner(result, future, yielded)
Runner会将yielded加入到io_loop, 等待future完成调用run方法
```python
....
else:
    try:
        self.future = convert_yielded(yielded)
    except BadYieldError:
        self.future = TracebackFuture()
        self.future.set_exc_info(sys.exc_info())

if not self.future.done() or self.future is moment:
    self.io_loop.add_future(
        self.future, lambda f: self.run())
    return False
return True
```
        
         
### io_loop.add_future
```python
def add_future(self, future, callback):
    """Schedules a callback on the ``IOLoop`` when the given
    `.Future` is finished.

    The callback is invoked with one argument, the
    `.Future`.
    """
    assert is_future(future)
    callback = stack_context.wrap(callback)
    future.add_done_callback(
        lambda future: self.add_callback(callback, future))
```

### Runner.run()
这里会通过self.gen.send(value)方法,接着执行剩下的代码。
```python
#这里的future为自定义future
try:
    value = future.result()
except Exception:
    self.had_exception = True
    exc_info = sys.exc_info()

if exc_info is not None:
    yielded = self.gen.throw(*exc_info)
    exc_info = None
else:
    yielded = self.gen.send(value)
```


## IOLoop
IOLoop 主要利用select + pipe 实现了一个高效的事件机制的死循环,用来不停的执行回调函数。 我们完全可以利用while true + time.sleep 实现类似功能,但效果可以脑补,自然很差。 
而tonado的ioloop 根据不同服务器使用了不同的实现方式。
```

@classmethod
def configurable_default(cls):
    if hasattr(select, "epoll"):
        from tornado.platform.epoll import EPollIOLoop
        return EPollIOLoop
    if hasattr(select, "kqueue"):
        # Python 2.6+ on BSD or Mac
        from tornado.platform.kqueue import KQueueIOLoop
        return KQueueIOLoop
    from tornado.platform.select import SelectIOLoop
    return SelectIOLoop
```        



为了简化源码分析的难度, 我做了一个超级简化版本的IOLoop。主要包含两大块:

+ select + pipe 实现的事件机制的死循环
    - 首先,当然是while True
    - select 监听 pipe 的read 文件描述符
    - select 唤醒后,消费完pipe 中所有消息
    - 添加回调函数方法, 会往pipe 中写消息,唤醒select,使其能处理callback
    
+ 一个子线程不停往ioloop添加回调函数



```python
# coding=utf-8

import copy
import fcntl
import functools
import os
import select
import threading
import time


def _set_nonblocking(fd):
    flags = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)


class Waker(object):
    def __init__(self):
        r, w = os.pipe()
        # 启用非阻塞模式,方便消费完成后退出
        _set_nonblocking(r)
        _set_nonblocking(w)
        self.reader = os.fdopen(r, "rb", 0)
        self.writer = os.fdopen(w, "wb", 0)

    def fileno(self):
        return self.reader.fileno()

    def write_fileno(self):
        return self.writer.fileno()

    def wake(self):
        try:
            print 'wake.....up, send out a b"x"!'
            self.writer.write(b"x")
        except IOError:
            pass

    def consume(self):
        try:
            print 'consume all wake up signal, it is b"x"'
            while True:
                result = self.reader.read()
                if not result:
                    break

        except IOError as e:
            print e.args
            pass

    def close(self):
        self.reader.close()
        self.writer.close()


class IoLoop(object):
    _EPOLLIN = 0x001
    _EPOLLPRI = 0x002
    _EPOLLOUT = 0x004
    _EPOLLERR = 0x008
    _EPOLLHUP = 0x010
    _EPOLLRDHUP = 0x2000
    _EPOLLONESHOT = (1 << 30)
    _EPOLLET = (1 << 31)

    # Our events map exactly to the epoll events
    NONE = 0
    READ = _EPOLLIN
    WRITE = _EPOLLOUT
    ERROR = _EPOLLERR | _EPOLLHUP

    def __init__(self):
        self._callbacks = []
        self._waker = Waker()
        self._impl = select.epoll()
        self._handler = lambda fd, events: self._waker.consume()
        
        # 将warker 的读文件描述符注册至select,监听 READ 和 ERROR 事件
        self._impl.register(self._waker.fileno(), self.READ | self.ERROR)

    def add_callback(self, callback, *args, **kwargs):
        # 利用functools.partial添加回调函数, 在毁掉函数为空的情况下唤醒ioloop
        list_empty = not self._callbacks
        self._callbacks.append(functools.partial(
            callback, *args, **kwargs))
        if list_empty:
            self._waker.wake()

    def start(self):

        while True:
            # 执行毁掉函数
            callbacks = copy.copy(self._callbacks)
            self._callbacks = []
            print 'run callback: ', callbacks
            for callback in callbacks:
                callback()

            # 回调函数运行结束, 继续监听pipe
            print 'waiting new callback'
            event_pairs = self._impl.poll(3600)
            for event_pair in event_pairs:
                fd, events = event_pair
                print fd, events
                
                # 接收到任何消息, 调用consume,消费所有消息, 这时候,下次循环时会开始执行回调函数
                handler = self._handler
                handler(fd, events)


def test(a, b):
    print 'run callback function test, args:', a, b


def test_add_callback(ioloop):
    while True:
        print 'add callback'
        ioloop.add_callback(test, 888, 999)
        time.sleep(10)


def test_ioloop():
    ioloop = IoLoop()

    print 'add a callback function'
    ioloop.add_callback(test, 2, 2)

    print 'start a thread to add callback function'
    thread = threading.Thread(target=test_add_callback, name='test_add_callback', args=(ioloop,))
    thread.daemon = True
    thread.start()

    print 'start ioloop'
    ioloop.start()


if __name__ == '__main__':
    test_ioloop()
```