Date: 2016-08-03
Title: fabric 安装salt minions
Tags: Salt
sulg: fabric_install_salt_minion


salt 需要安装客户端, 写了一个简单的fabric 脚本进行安装, 大规模安装可能还需要进行一些优化

cat fabric-salt.py

```
#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from fabric.api import *


env.roledefs = {
    'all': [
     '1.1.1.1'
    ]
}

f = file('.password')
env.password = f.readline().strip()
f.close()


@roles('all')
@parallel(pool_size=8)
def install_slat():
    sudo('pip install -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com salt')

    sudo("mkdir -p /etc/salt")
    sudo("echo 'master: 10.142.103.177' > /etc/salt/minion")
    sudo('scp -o "StrictHostKeyChecking no" yihan@36.110.210.15:/etc/init.d/salt-minion /etc/init.d/salt-minion ')
    sudo('chkconfig salt-minion on')

    sudo('hostname > /etc/salt/minion_id')
    sudo('cat /etc/salt/minion_id')

    sudo('service salt-minion restart')
```