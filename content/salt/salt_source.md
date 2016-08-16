Date: 2016-08-10
Title: salt - LocalClient 源码解析
Tags: Salt
sulg: salt_source

salt 源码点滴记录

## 最简单的操作LocalClient
想看看salt的源码, 从最简单的操作开始。 其实restful api, 命令行,还是python api,都殊途同归,最后也会到达salt.client, 只是入口不一样, restful API入口是 salt.netapi,
而命令行的入口是 salt.cli。 
```
# 变更虚拟环境
source /u01/virtualenv/salt/bin/activate
```

```python
import salt.client

local = salt.client.LocalClient()
local.cmd('*', 'test.fib', [10])

```


## /u01/github/salt-develop/salt/client/__init__.py : class LocalClient

### __init__()
主要初始化了上下文, 然后啥也没干,细节先TODO,后续再补
```python
# c_path: 主要是master配置文件所在,一般是/etc/salt/master ,一般不填
# mopts: 如果有值,则忽略c_path ,这两个参数主要是搞定 self.opts
# skip_perm_errors: 权限校验 TODO
# io_loop: TODO
def __init__(self,
                 c_path=os.path.join(syspaths.CONFIG_DIR, 'master'),
                 mopts=None, skip_perm_errors=False,
                 io_loop=None):
               
        # self.opts 所有的配置项
        if mopts:
            self.opts = mopts
        else:
            if os.path.isdir(c_path):
                log.warning(
                    '{0} expects a file path not a directory path({1}) to '
                    'it\'s \'c_path\' keyword argument'.format(
                        self.__class__.__name__, c_path
                    )
                )
            self.opts = salt.config.client_config(c_path)
            
        # 其他细节 TODO
        self.serial = salt.payload.Serial(self.opts)
        
        self.salt_user = salt.utils.get_specific_user()
        
        self.skip_perm_errors = skip_perm_errors
        
        self.key = self.__read_master_key()
        
        # 用于获取返回
        self.event = salt.utils.event.get_event(
                'master',
                self.opts['sock_dir'],
                self.opts['transport'],
                opts=self.opts,
                listen=False,
                io_loop=io_loop)
                
        self.utils = salt.loader.utils(self.opts)
        self.functions = salt.loader.minion_mods(self.opts, utils=self.utils)
        self.returners = salt.loader.returners(self.opts, self.functions)

```

#### 主要上下文 【TODO】:  
* self.opts
* self.utils
* self.key
* self.salt_user
* self.skip_perm_errors
* self.event  # 用于获取命令返回
* self.utils
* self.functions
* self.returners
* self.serial # 序列化, 关心的配置为serial ,默认是 msgpack 




### cmd()
为了了解整个流程,而不是去纠结各种执行方式,比如批次执行,异步执行等等, 就看cmd吧。  
cmd 参数很好理解, 主要做了两个事情, 执行任务run_job, 返回 pub_data, pub_data 中主要有job_id和minions, 用于从event中获取到返回结果,
返回结果是一个minion_id 为key 的字典。 代码量很少,就粘贴在下面了。
```python
# tgt, expr_form 确定minins
# fun arg timeout 确定命令执行
# ret 指定return
# jid 指定jid
# kwarg
# kwargs 权限相关参数
def cmd(
        self,
        tgt,
        fun,
        arg=(),
        timeout=None,
        expr_form='glob',
        ret='',
        jid='',
        kwarg=None,
        **kwargs):
    arg = salt.utils.args.condition_input(arg, kwarg)
    pub_data = self.run_job(tgt,
                            fun,
                            arg,
                            expr_form,
                            ret,
                            timeout,
                            jid,
                            **kwargs)

    if not pub_data:
        return pub_data

    ret = {}
    for fn_ret in self.get_cli_event_returns(
            pub_data['jid'],
            pub_data['minions'],
            self._get_timeout(timeout),
            tgt,
            expr_form,
            **kwargs):

        if fn_ret:
            for mid, data in six.iteritems(fn_ret):
                ret[mid] = data.get('ret', {})

    return ret
```


###run_job()

```python
def run_job(
            self,
            tgt,
            fun,
            arg=(),
            expr_form='glob',
            ret='',
            timeout=None,
            jid='',
            kwarg=None,
            **kwargs):
    arg = salt.utils.args.condition_input(arg, kwarg)

    try:
        pub_data = self.pub(
            tgt,
            fun,
            arg,
            expr_form,
            ret,
            jid=jid,
            timeout=self._get_timeout(timeout),
            **kwargs)
    except SaltClientError:
        # Re-raise error with specific message
        raise SaltClientError(
            'The salt master could not be contacted. Is master running?'
        )
    except Exception as general_exception:
        # Convert to generic client error and pass along message
        raise SaltClientError(general_exception)

    return self._check_pub_data(pub_data)
```

### pub()
参数很好理解,跟之前的参数一样
```python
def pub(self,
        tgt,
        fun,
        arg=(),
        expr_form='glob',
        ret='',
        jid='',
        timeout=5,
        **kwargs):
```

根据ipc_mode选择了通讯方式,是tcp还是ipc, 一般windows 下是 tcp, 而linux 则是ipc
```python
        if (self.opts.get('ipc_mode', '') != 'tcp' and
                not os.path.exists(os.path.join(self.opts['sock_dir'],
                'publish_pull.ipc'))):
            log.error(
                'Unable to connect to the salt master publisher at '
                '{0}'.format(self.opts['sock_dir'])
            )
            raise SaltClientError
```

组装通讯用的data, 主要处理了tgt和expr_from,
```python
payload_kwargs = self._prep_pub(
                tgt,
                fun,
                arg,
                expr_form,
                ret,
                jid,
                timeout,
                **kwargs)
                
# 结果, 如果使用syndic模式, 需要将user和timeout传递下去
payload_kwargs = {'cmd': 'publish',
                          'tgt': tgt,
                          'fun': fun,
                          'arg': arg,
                          'key': self.key,
                          'tgt_type': expr_form,
                          'ret': ret,
                          'jid': jid,
                          ####
                          'kwargs':kwargs,
                          'user': kwargs['user'] if self.opts['syndic_master'] else self.salt_user,
                          'to': timeout if self.opts['order_masters']
                          }
```

获取channel, 这里使用了warp,做了一些封装, 上述例子最终使用的是 AsyncZeroMQReqChannel, 
```python

# master url, 此处的ip 为master 本机ip: 0.0.0.0 , 端口为4506, 这个端口是用来minions 返回结果用的
master_uri = 'tcp://' + salt.utils.ip_bracket(self.opts['interface']) + \
                     ':' + str(self.opts['ret_port'])
channel = salt.transport.Channel.factory(self.opts,
                                                 crypt='clear',
                                                 master_uri=master_uri)
                                                 
                                                 
```

AsyncZeroMQReqChannel 细节往后看, 这里接着看run_job, 将消息发送给zeromq 4506 端口后, 会检查其结果。 

### _check_pub_data(pub_data)
主要做了两件事情, 一是检查jid是否正常, 二是subscribe event获取执行结果。 


### get_cli_event_returns()
通过event获取结果, 主要通过event_tag 筛选消息。程序会连接到 zmq pub socket上, 通过tag解析不同类型的event。

job tag 类似 salt/job/jid, 如果是syndic, 则类似于 syndic/.*/jid
```python

TAGEND = '\n\n'  # long tag delimiter
TAGPARTER = '/'  # name spaced tag delimiter
SALT = 'salt'  # base prefix for all salt/ events
# dict map of namespaced base tag prefixes for salt events
TAGS = {
    'auth': 'auth',  # prefix for all salt/auth events
    'job': 'job',  # prefix for all salt/job events (minion jobs)
    'key': 'key',  # prefix for all salt/key events
    'minion': 'minion',  # prefix for all salt/minion events
                         # (minion sourced events)
    'syndic': 'syndic',  # prefix for all salt/syndic events
                         # (syndic minion sourced events)
    'run': 'run',  # prefix for all salt/run events (salt runners)
    'wheel': 'wheel',  # prefix for all salt/wheel events
    'cloud': 'cloud',  # prefix for all salt/cloud events
    'fileserver': 'fileserver',  # prefix for all salt/fileserver events
    'queue': 'queue',  # prefix for all salt/queue events
}
```


subscribe 主要是添加一个tag 名称, 和match 用的fuction
```python
    def subscribe(self, tag=None, match_type=None):
        '''
        Subscribe to events matching the passed tag.

        If you do not subscribe to a tag, events will be discarded by calls to
        get_event that request a different tag. In contexts where many different
        jobs are outstanding it is important to subscribe to prevent one call
        to get_event from discarding a response required by a subsequent call
        to get_event.
        '''
        if tag is None:
            return
        match_func = self._get_match_func(match_type)
        self.pending_tags.append([tag, match_func])
```


get_event 优先通过 _check_pending 检查pending_events, 如果存在则放回,如果不存在,则调用_get_event 获取消息,  
如果直接match上了,则返回,那些没有match上当前tag,但是match上其他tag的,放置到 pending_events 列表中,什么也没match上的直接丢弃。处理过程中,也会将 unsubscribe的event移除。
```python
def _get_event(...):
...
            if not match_func(ret['tag'], tag):
                # tag not match
                if any(pmatch_func(ret['tag'], ptag) for ptag, pmatch_func in self.pending_tags):
                    log.trace('get_event() caching unwanted event = {0}'.format(ret))
                    self.pending_events.append(ret)
                if wait:  # only update the wait timeout if we had one
                    wait = timeout_at - time.time()
                continue
```


## 上面只是整体的一个执行流程, 还缺少salt transport 部分, event 部分, client端等处理。 

