Date: 2016-08-08
Title: Tornado Test
Tags: Python, Tornado
sulg: tornado_test



看salt源码,发现用了一些tornado的异步编程, 写了点测试代码。


### 首先熟悉下简单的yield send, 通过send发送数据至生成器。
```
In [16]: def test_yield():
   ....:         print "test yeild"
   ....:         says = yield
   ....:         print says
   ....:

In [17]: y = test_yield()

In [18]: y.next()
test yeild

In [19]: y.send('a')
a
---------------------------------------------------------------------------
StopIteration                             Traceback (most recent call last)
<ipython-input-19-cf1d6ef756f2> in <module>()
----> 1 y.send('a')

StopIteration:
```

