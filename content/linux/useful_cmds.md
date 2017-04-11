Date: 2015-10-29
Title: 命令-赶紧的
Tags: Linux
Slug: Linux

##查看端口的占用情况
```
netstat -tln
lsof -i:80  
```

##查看32,64位系统
```
getconf LONG_BIT
```


## 去除注释，空行
```
more php-fpm.conf | grep -v ^\; | grep -v ^$;
```

## 查看tcp连接情况
```
netstat -n|awk '/^tcp/{++S[$NF]}END{for (key in S) print key,S[key]}'
```

## CPU使用率高
```
# top 获取 pid
# gstack 获取stack trace
# gstack 12594 >> /tmp/gstack.rst
# top 查看最大消耗的线程号
# top -H -p 12594 
# /tmp/gstack.rst 文件中查看线程号


```


