Date: 2016-08-10
Title: 跟着salt学单例模式
Tags: Salt
sulg: salt_source


/u01/github/salt-develop/salt/transport/zeromq.py 里使用了单例模式, 写了一个模板类, 需要使用时直接修改添加方法就好了。


单例模式一般离不开6个方面的内容, 存储, 创建实例, 获取唯一key, 初始化(一般为空), 单例初始化操作,  删除
```python
# coding=utf-8
import logging
import weakref

log = logging.getLogger(__name__)


class SingletonClass(object):
    # 使用weakref.WeakKeyDictionary来存储实例,weakref 中的item会在没有其他引用时被删除,GOOD
    instance_map = weakref.WeakValueDictionary()

    def __new__(cls, *args, **kwargs):
        '''
        Only create one instance of channel per __key()
        '''

        # 获取key
        key = cls.__key(*args, **kwargs)

        if key not in cls.instance_map:

            new_obj = object.__new__(cls)
            new_obj.__singleton_init__(*args, **kwargs)
            cls.instance_map[key] = new_obj
            log.debug(
                'Create new object for key {0}'.format(key))
        else:
            log.debug('Re-using for {0}'.format(key))
        try:
            return cls.instance_map[key]
        except KeyError:
            # In iterating over the loop_instance_map, we may have triggered
            # garbage collection. Therefore, the key is no longer present in
            # the map. Re-gen and add to map.
            log.debug('Create new object due to GC for key {0}'.format(key))
            new_obj = object.__new__(cls)
            new_obj.__singleton_init__(*args, **kwargs)
            cls.instance_map[key] = new_obj
            return cls.instance_map[key]

    @classmethod
    def __key(cls, *args, **kwargs):
        return ('.'.join(args),  # where the keys are stored
                '.'.join(kwargs.keys()),  # minion ID
                '.'.join(kwargs.values())
                )

    # has to remain empty for singletons, since __init__ will *always* be called
    def __init__(self, *args, **kwargs):
        pass
        # do nothing

    # an init for the singleton instance to call
    def __singleton_init__(self, *args, **kwargs):
        self.dummy = 'dummy'
        # do something

    # 对于socket等资源,可以考虑进行删除, 如果没有特殊的需要移除,继承时需要注意,需要手工调用父类的__del__
    def __del__(self):
        pass


    def do_something(self):
        pass



class SingletonManager():
    @staticmethod
    def instance(*args, **kwargs):
        return SingletonClass(*args, **kwargs)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    a = SingletonManager.instance('a', 'b', c='c')
    a = 'abc'
    b = SingletonManager.instance('a', 'b', c='c')
    c = SingletonManager.instance('a', 'b', c='c')
    d = SingletonManager.instance('a', 'b', c='c')
    print a, b, c, d

```