Date: 2016-03-20
Title: Pandas
Tags: Python, Pandas
sulg: pandas

## 简单操作
```
# 设置索引
basic = basic.set_index('code')

#左连接
rst = basic.join(max, how='left')

#多次左连接，设置右边前缀
rst = rst.join(min, how='left', rsuffix='min')

#简单计算
rst['grow'] = rst['high'] / rst['lowmin']

#四舍五入
rst['round_grow'] = rst['grow'].apply(numpy.round)

# 选择列
rst = rst[['name', 'grow','round_grow']]

#排序
rst = rst.sort_values('grow')

#to_csv
rst.to_csv(os.path.join('/xxx', 'xxx.csv'))


#合并结果
df = pd.concat(df_list)

```


# 聚合操作
```
# group by, 取最大值，最小值, 数量
df = pd.read_csv('xxx.csv')
g = df.groupby(['code'])
max = g.max()
min = g.min()
cnt = g.count()


```



# 数据选择分片
```
# 根据特定列选择数据
df = df[df['date'] >= begin]
df = df[df['date'] <= end]


# 根据索引选择特定列的值
df.loc[i, ['industry']]
industry = str(base_info[0])
```

