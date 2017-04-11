title: EBS服务启动失败处理一粒
slug: oracle_start
date: 2016-10-25



先stop然后做以下操作再启动应该就好，里面有一些不知道是啥缓存的文件吧，其中后缀是.lock的就是报错的原因，只要把这些lock的删掉就行，都删了也没问题

```
rm -rf $ORA_CONFIG_HOME/10.1.3/j2ee/oacore/persistence/*
rm -rf $ORA_CONFIG_HOME/10.1.3/j2ee/oafm/persistence/*
rm -rf $ORA_CONFIG_HOME/10.1.3/j2ee/forms/persistence/*
```