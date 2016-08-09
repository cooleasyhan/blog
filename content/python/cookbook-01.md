Date: 2016-6-11
Title: Cookbook-数据结构和算法
Tags: Python, Cookbook
sulg: cookbook1

## 1.1 序列分解 
_, x, y = (3, 4, 5)

x, *y, z = (3, 4, 5, 6)

x, *_, z = (3, 4, 5, 6, 7)

## 1.2 collection  

### 1.2.1 collection.deque  
deque: 保留历史记录  
deque(maxlen=5)

### 1.2.2 collection.defaultdict  
一个key对应多个值  

### 1.2.3 collection.orderdict
按照添加顺序排序 


### 1.2.4 collection.Counter
```
from collection import Counter
_list = list()
counter = Counter(_list)
print counter['key']  # 1
counter['key'] += 1 # 增加计数
counter.update(_new_list)


countera + acountb  # 可进行简单加减乘除
countera - counterb


```

## 1.2.5 collection.namedtuple()
```

from collection import namedtuple
User = namedtuple('User',['user_id', 'name'])
user = User(1,'yh')

print user.user_id, user.name
for user in [(1, 'yh'),(2,'yh2')]:
    u = User(*user)
    print u.user_id
    

# dict_to_namedtuple
dict_a = {'user_id':3, 'name':'yh3'}
# 通过_replace 设置默认值
user_prototype = {'user_id':0, 'name':None}  
user3 = user_prototype._replace(**dict_a)  

```


## 1.2.6 collection.ChainMap()
from collection import ChainMap  
将多个字典拼接成一个字典,通过迭代器实现,返回遇到的第一个值  
```
from collection import ChainMap
a={'x':1, 'y':2}
b={'x':3, 'z':3}

c = ChainMap(a, b)
print c['x'] # 1


# 可以将一个key值多个值按照链表保存并取出
v = ChainMap()
v['x'] = 1
v = v.new_child()
v['x'] = 2

print v['x'] #2
print v.parents['x']
```


## 1.3 heapq

### 1.3.1 找到最大活最小的N个元素  
import heapq  
heapq.nsmallest  
q = heapq.nlargest(3, data_list_or_dict, key=lambda s: s['key'])  


### 1.3.2 实现优先队列
heapq.heappush(_queue, priority, index, item)  
index: 用于在同优先级的item间排序  
heapq.heappop(self._queue)[-1]  

## 1.4 zip
注意: zip 结果是迭代器  
计算dict的最大值最小值,排序  
min(zip(_dict.values(), _dict.keys()))  
sorted(zip(_dict.values(), _dict.keys()))  


## 1.5 dict
### 1.5.1 字典比较
同时存在 _dicta.keys() & _dictb.keys()  
a中存在b不存在 _dicta.keys() - _dictb.keys()  

_dicta.items() & _dictb.items()  

将结果组装成字典
c = {key: dict_a[key] for key in dict_a.keys() - dict_b.keys()}  

### 1.5.2 defaultdict 见 1.2.2 collection.defaultdict  

## 1.6 从序列中移除重复项,且顺序不变
利用迭代器和set  
```
def dedupe(items, fun=None):
    _set = set()
    for item in items:
        var = item is fun is None else fun(item)
        if var not in _set:
            yield item
            _set.add(var)
        
rst = list(dedupe([1,3,4,4,5]))

```

## 1.7 对切片命名
S=slice(1,2)  
S 属性:  
S.start  
S.stop  
S.step  
rec=_list[S]  

### 按照特定长度切片
indices(size)  


## 1.8 字典排序----itemgetter
from operator import itemgetter  
可以用于排序, 最大值,最小值。 也可以用lambda  
sorted min max
```
#等同于下面代码
def itemgetter(*items):
    if len(items) == 1:
        item = items[0]
        def g(obj):
            return obj[item]
    else:
        def g(obj):
            return tuple(obj[item] for item in items)
    return g

```

sorted(_dict, key=itemgetter(('key','key1','key2')))


## 1.9 object 排序--attrgetter  
可以用于sorted, max, min  
from operator import attrgetter  

sorted(_dict, key=attrgetter('attr1'))  



## 1.10 itertools
### 1.10.1 groupby
groupby 需要先排序, 结果是迭代器, 也可以使用collection.defaultdict 实现,不需要排序  

```
from itertools import groupby
from operator import itemgetter

rows=[dict1, dict2, dict3]

rows.sort(key=itemgetter('date'))
for date, items in groupby(rows, key=itemgetter('date')):
    pass
    
```

### 1.10.2 compress
多个列表组合删选
```
list_a = ['a','b','c','d']
list_b = [-1, 0, 1, 2]

from itertools import compress
more0 = [n > 0 for n in list_b] # [False, False, True, True]

list(compress(list_a, more0)) # ['c','d']


```

## 1.11 筛选序列中的元素
rst = [n in list_n if n < 0]  
rst = list(filter(fun_is_int, list_n))  

### 1.11.1 多个列表组合删选 
from itertools import compress # 详情见 1.10.2 compress

### 1.11.2 刷选后直接进行换算,比如min, max
min(n in list_n if n < 0)  
min([n in list_n if n < 0]) # 该语句多一个将迭代器转换成列表的操作


## 1.12 字典提取子集---字典推导式
pl = dict((key, value) for key, value in dict_a.items() if value > 100)   

list_keys = ['a','b','c']  
pl = {key:dict_a[key] for key in dict_a.keys() & list_keys}  

