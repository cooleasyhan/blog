date: 2015-11-16
author: YiHan
title: 排序算法python实现
tags: Algorithms, sort, python
slug: sort_code

##Code
SelectSort 选择排序  
InsertionSort, InsertionSort 插入排序  
ShellSort, ShellSort2 希尔排序  
HeapSort 堆排序  
```
# -*- coding: UTF-8 -*-
'''sort base class'''
import random
import time

LIST_A = list()
for i in range(10000):
    LIST_A.append(random.randint(1, 100))


class TimeIt(object):

    def __init__(self):
        pass

    def __call__(self, fn):
        def wrapped(*args, **kwargs):
            begin = time.time()
            fn(*args, **kwargs)
            end = time.time()
            print '    Time:' + str(end - begin)
        return wrapped


class Bar(object):

    @classmethod
    def show(cls, datas):
        import matplotlib
        import time
        import matplotlib.pyplot as plt
        from numpy import array

        matplotlib.use('TKAgg')

        def animated_barplot():
            # http://www.scipy.org/Cookbook/Matplotlib/Animations

            x = array(datas[0])
            print x
            rects = plt.bar(range(len(x)), x,  align='center')
            for i in range(1, len(datas)):
                print datas[i]
                x = array(datas[i])
                for rect, h in zip(rects, x):
                    rect.set_height(h)
                fig.canvas.draw()
                time.sleep(1)

        fig = plt.figure()
        win = fig.canvas.manager.window
        win.after(100, animated_barplot)
        plt.show()


class BaseSort(object):
    steps = list()

    '''BaseSort'''

    @classmethod
    def prepare_list(cls):
        '''prepare_list'''

        return LIST_A

    def sort(self, list_a):
        '''sort'''
        raise NotImplementedError

    @classmethod
    def exch(cls, list_a, i, j):
        '''exch'''
        tmp = list_a[i]
        list_a[i] = list_a[j]
        list_a[j] = tmp

    @classmethod
    def show(cls, list_a):
        '''show'''
        # print '   ', list_a

    @classmethod
    def is_sorted(cls, list_a):
        '''is_sorted'''
        for i in range(1, len(list_a)):
            if list_a[i] < list_a[i - 1]:
                return False

        return True

    def main(self):
        '''main'''

        list_a = []
        list_a = self.prepare_list()
        self.sort(list_a)
        assert self.is_sorted(list_a)
        self.show(list_a)
        # print BaseSort.steps
        # if len(BaseSort.steps) > 1:
        #    Bar.show(BaseSort.steps)


class SelectSort(BaseSort):

    '''
    SelectSort
    
    逐个循环, 当前元素与后续所有元素比较,得到最小值,与当前元素互换
    
    
    '''
    @TimeIt()
    def sort(self, list_a):

        length = len(list_a)
        if length == 0:
            return

        for i in range(0, length):
            min_value = list_a[i]
            min_index = i
            for j in range(i, length):
                if min_value <= list_a[j]:
                    pass
                else:
                    min_value = list_a[j]
                    min_index = j

            self.exch(list_a, i, min_index)
            BaseSort.steps.append(list(list_a))


class InsertionSort(BaseSort):

    '''
    InsertionSort
    一句话: 扫描每个key, 在前面找一个能放下的地方, 后面的牌靠后站一位
    
    从第二个元素开始循环, 与之前所有元素进行比较,如果找到可以插入的位置, 
    则将插入位置后的所有元素向后偏移一位, 将当前元素值替换到插入位置
    3 1 9 7 2 4 8
    1 3 9 7 2 4 8
    1 3 9 7 2 4 8
    1 3 7 9 2 4 8
    1 2 3 7 9 4 8
    1 2 3 4 7 9 8
    1 2 3 4 7 8 9
    
    
    '''
    @TimeIt()
    def sort(self, list_a):
        length = len(list_a)
        if length == 0:
            return

        for i in range(1, length):
            key = list_a[i]
            index = i
            for j in range(0, i):  # find insert index
                if list_a[j] > list_a[i]:
                    index = j
                    break
            for k in range(i, index, -1):
                list_a[k] = list_a[k - 1]

            list_a[index] = key


class InsertionSort2(BaseSort):

    '''InsertionSort'''
    一句话: 扫描每个key, 与前面的骗进行比较,如果小就交换
    
    3 1 9 7 2 4 8
    1 3 9 7 2 4 8
    1 3 9 7 2 4 8
    1 3 7 9 2 4 8
        1 3 7 2 9 4 8
        1 3 2 7 9 4 8
        1 2 3 7 9 4 8
    1 2 3 7 9 4 8
    1 2 3 4 7 9 8
    1 2 3 4 7 8 9
    
    @TimeIt()
    def sort(self, list_a):
        length = len(list_a)
        if length == 0:
            return

        for i in range(1, length):
            for k in range(i, 0, -1):
                if list_a[k] < list_a[k - 1]:
                    self.exch(list_a, k, k - 1)
                else:
                    break


class ShellSort(BaseSort):

    '''
    ShellSort
    分组进行插入排序,然后降低分组数再进行插入排序,直到所有元素进行一次插入排序。
    插入排序对近似排序的队列有很好的性能, 分组数按照3的倍数递增
    第一次分组是4, 第二次分组是1 
    
    h = 4
    
    3 1 9 7 2 4 8
    2 1 9 7 3 4 8
    2 1 9 7 3 4 8
    2 1 8 7 3 4 9
    
    h = 1
    1 2 8 7 3 4 9
    1 2 8 7 3 4 9
    1 2 7 8 3 4 9
    1 2 3 7 8 4 9
    1 2 3 4 7 8 9
    
    
    
    '''
    @TimeIt()
    def sort(self, list_a):
        length = len(list_a)
        if length == 0:
            return

        h = 1
        while h < length / 3:
            h = 3 * h + 1

        while h >= 1:
            for i in (0, h):
                for i in range(i, length, h):
                    for k in range(i, 0, -1 * h):
                        if list_a[k] < list_a[k - 1]:
                            self.exch(list_a, k, k - h)
                        else:
                            break
            h = h / 3


class ShellSort2(BaseSort):

    '''ShellSort2'''
    @TimeIt()
    def sort(self, list_a):
        length = len(list_a)
        if length == 0:
            return

        h = 1
        while h < length / 3:
            h = 3 * h + 1

        while h >= 1:
            for i in range(h, length):
                for k in range(i, 0, -1):
                    if list_a[k] < list_a[k - h]:
                        self.exch(list_a, k, k - h)
                    else:
                        break

            h = h / 3


class HeapSort(BaseSort):
    '''
    HeapSort
    堆排序, 如果父节点均大于或小于子节点就是堆了。 一次堆处理总能得到一个最大值或者最小值。 
    
    首先构建一个堆, 逐个检查所有的父节点, 并将父节点下放
    
    将堆顶点数据与最后节点进行交换,然后对顶点进行下放
    '''

    def _parent(self,  j, k, i):
        idx = (i + 1) / 2 - 1
        if j <= idx <= k:
            return idx
        else:
            return None

    def size(self):
        return len(self._list)

    def _left_child(self, j, k, i):
        idx = i * 2 + 1
        if j <= idx <= k:
            return idx
        else:
            return None

    def _right_child(self, j, k, i):
        idx = i * 2 + 2
        if j <= idx <= k:
            return idx
        else:
            return None

    def _bigger_child(self, list_a, j, k, i):
        left_idx = self._left_child(j, k, i)
        right_idx = self._right_child(j, k, i)
        if left_idx is None and right_idx is None:
            return None
        if right_idx is None:
            bigger_idx = left_idx
        elif list_a[left_idx] > list_a[right_idx]:
            bigger_idx = left_idx
        else:
            bigger_idx = right_idx

        return bigger_idx

    def _exch(self, list_a, i, j):
        list_a[i], list_a[j] = list_a[j], list_a[i]

    def sink(self, list_a, j, k):
        i = j
        bigger_idx = self._bigger_child(list_a, j, k, i)
        while bigger_idx is not None:

            if list_a[bigger_idx] > list_a[i]:
                self._exch(list_a, bigger_idx, i)
                i, bigger_idx = bigger_idx, self._bigger_child(
                    list_a, j, k, bigger_idx)
            else:
                break

    @TimeIt()
    def sort(self, list_a):
        l = len(list_a)
        i = self._parent(0, l - 1, l - 1)
        while i >= 0:
            self.sink(list_a, i, l - 1)
            i -= 1

        while l > 0:
            self._exch(list_a, 0, l - 1)
            l -= 1
            self.sink(list_a, 0, l - 1)

if __name__ == '__main__':
    for sort in (SelectSort(), InsertionSort(), InsertionSort2(),
                 ShellSort(), ShellSort2(), HeapSort()):
        print sort.__class__
        sort.main()
        pass

    # sort = SelectSort()
    # sort.main()

```
