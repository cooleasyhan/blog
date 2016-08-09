Date: 2015-10-29
Title: 命令-赶紧的
Tags: Linux
Slug: Linux

##查看端口的占用情况
netstat -tln

##查看32,64位系统
getconf LONG_BIT

## 去除注释，空行
more php-fpm.conf | grep -v ^\; | grep -v ^$;


## 查看tcp连接情况
netstat -n|awk '/^tcp/{++S[$NF]}END{for (key in S) print key,S[key]}'

