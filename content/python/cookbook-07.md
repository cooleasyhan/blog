Date: 2016-6-26
Title: Cookbook-函数
Tags: Python, Cookbook
sulg: cookbook7

## 7.1 编写可接受任何参数的函数
*args, **kwargs  
args 只能是最后一个位置参数。
```
def fun(x, *args, y, **kwargs):
    '''
    y 是keyword参数
    '''
    pass
```

## 7.2 只接受关键字参数

```
def fun(x, *, block):
    '''
    y 是keyword参数
    '''
    pass
    
fun(x, block=True)
fun(x, True) # TypeError
```

## 7.3 设置元数据类型

```
def fun(x:int, *, block:boolean) -> int:
    '''
    y 是keyword参数
    '''
    pass
    
fun(x, block=True)
fun(x, True) # TypeError
```

## 7.4 返回多个值


## 7.5 带默认值的函数
7.5.1 可以通过no_object = object(),来设定空的默认值。避免使用Flase, None
7.5.2 默认值只在函数初始化时生效一次,所以尽量不要使用变量作为默认值
7.5.3 不要使用地址引用作为参数传递

## 7.6 匿名函数 lambda, 7.7 匿名函数绑定变量的值
需要注意的是匿名函数的值是在真正调用的时候才进行赋值,如果需要在定义的时候就进行赋值,需要使用默认参数
```

In[14]: x = 10
In[15]: a = lambda y : x + y
In[16]: x = 20
In[17]: b = lambda y : x + y
In[18]: a(10)
Out[18]: 30
In[19]: b(10)
Out[19]: 30
In[20]: x = 10
In[21]: a = lambda y, x=x : x + y
In[22]: x = 20
In[23]: b = lambda y, x=x : x + y
In[24]: a(10)
Out[24]: 20
In[25]: b(10)
Out[25]: 30

```

## 7.8 让带有N个参数的函数以更少参数调用
```
from functools import partial
def spam(a,b,c,d):
    print a,b,c,d
    
s1 = partial(spam, 1)
s1(2,3,4)

s2 = partial(spam, 1,2,d=33)
s2(3)

> 1 2 3 4
> 1 2 3 33

```


## 7.9 函数代替只有单个方法的类 ---- 闭包
```
class CTest(object):
    def __init__(self, para):
        self.para = para
    
    def do_something(self,a):
        print self.para, a
    
c = CTest('abc')
c.do_something(a='test')


def warp(para):
    _para = para
    def do_something(a):
        print _para, a
    
    return do_something
        
w = warp('abc')
w(a='test')

```

## 7.10 回调函数携带额外的状态类参数
1. 使用回调的方式写的代码会造成发起请求和处理结果之间出现割裂,上下文会丢失。  
2. 处理方式:  
    2.1 带状态参数的类
    2.2 闭包
    2.3 functools.partial , 利用partial封装一个状态类的class,统一处理, 也可以通过lambda处理
 
3. 代码示例略
 
 
## 7.11 内联回调函数
1. 



## 7.12 访问在闭包内变量的函数
在python3 之后有了nonloacl, 可以实现修改闭包中的变量
```
def test():
    a = None
    def fun():
        print a
    
    def get_a():
        return a
    
    def set_a(value):
        nonlocal a
        a = value
    
    fun.get_a = get_a
    fun.set_a = set_a
    return fun


```
    