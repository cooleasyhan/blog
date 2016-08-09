title: 主从同步
slug: mysql_skip
date: 2016-06-22

## 主从同步处理

最近mysql 主从经常出现不同步的情况。   
1. 从库开发修改,有同学上从库改表造成不同步。   
    处理: 从库设置为只读   
2. 主从同步hung住, 显示如下, 线程状态显示OK, 但是Seconds Behind Master 值非常大。  
```
Slave_IO_Running: Yes
Slave_SQL_Running: Yes
Seconds_Behind_Master: 9999

# 处理:  
stop slave; --等待时间可达数分钟
start slave;
```

3. 启用了gtid的主从同步,skip操作

获取当前 处理到的Executed_Gtid_Set, 下面最后处理的gtid 为: dcbfbf7e-e05a-11e5-8160-6c92bf225ad1:129985921
```
Retrieved_Gtid_Set: dcbfbf7e-e05a-11e5-8160-6c92bf225ad1:16700783-129985931
Executed_Gtid_Set: dc24de6f-2969-11e6-8ae8-6c92bf2c1069:1-11,
dcbfbf7e-e05a-11e5-8160-6c92bf225ad1:1-16132149:16700783-129985921
```      
通过创建空的gtid,跳过该gitd。

```
STOP SLAVE;
SET GTID_NEXT="dcbfbf7e-e05a-11e5-8160-6c92bf225ad1:129985921";
BEGIN; COMMIT;
SET GTID_NEXT="AUTOMATIC";
START SLAVE;
show slave status \G;
```


