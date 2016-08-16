Date: 2016-08-01
Title: salt配置
Tags: Salt
sulg: salt_setup



## master配置
master 主要配置file_roots, pillar_roots, 

```
# pam权限配置, 使用linux用户名密码进行登录
external_auth:
  pam:
    salt:
        - .*
        - '@runner'
        - '@wheel'
        
# master 是否可以接收minion文件,线上最好设置为False
file_recv: True
file_recv_max_size: 1000
        
# 文件目录
file_roots:
   base:
     - /srv/salt/base
   dev:
     - /srv/salt/dev
   prod:
     - /srv/salt/prod
     - /srv/formulas/redis-formula

# pillar 文件目录,与fie_roots对应
pillar_roots:
  base:
    - /srv/pillar/base
  prod:
    - /srv/pillar/prod
```

## salt 文件结构
目前使用多env结构。如nginx目录如下: files 存放源码, 通用配置文件, service init.d 脚本, map.jinja 存放相关跨平台mapping,如果有需要,可以merge pillar相关配置。
```
├── base
│   ├── init
│   │   ├── env_init.sls
│   │   ├── files
│   │   └── test_file_append.sls
│   └── top.sls
└── prod
    ├── nginx
    │   ├── files
    │   │   ├── nginx-1.8.1.tar.gz
    │   │   ├── nginx.conf
    │   │   └── nginx-init
    │   ├── install.sls
    │   ├── service.sls
    │   └── map.jinja
```

## top.sls 结构
```
base:
    '*':
        - init.env_init
prod:
    'xxxx':
        - nginx.service
        - php.install
        - php.php-redis
        - redis.server
```




## minion配置
如果使用mysql作为result, 需要设置mysql相关内容,并手工生成相关表  
https://docs.saltstack.com/en/latest/ref/returners/all/salt.returners.mysql.html#module-salt.returners.mysql  
```
cat /etc/salt/minion

master: 10.1.1.1
mysql.host: '1.1.1.1'
mysql.user: 'yihan'
mysql.pass: 'password123!'
mysql.db: 'salt'
mysql.port: 3306

cat /etc/salt/minion_id

hostname.x.x.x

```
