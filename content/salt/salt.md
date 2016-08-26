Date: 2016-08-01
Title: salt
Tags: Salt
sulg: salt

最近研究salt装我那小一百台服务器, 之前一直是fabric安装的, 感觉salt还是挺好用的, 下面是一些使用到的小脚本

## salt 常用命令
```sh
salt 'xxx*' state.show_lowstate
salt 'xxx*' state.show_highstate
salt '*' sys.doc state
salt '*' state.highstate
```

## salt formula
里头有很多软件安装的模板,通过pillar配置进行安装,需要一些个性化
https://github.com/saltstack-formulas  

## tips
1. 尽量使用name, 对每个小模块添加一个别名

## top.sls
```
base:
    '*':
        - init.env_init
prod:
    'xxx.xxx.xxx.xx':
        - nginx.service
        - php.install
        - php.php-redis
        - redis.server
```

## 应用入口文件demo 
init/env_init.sls
```
include:
    - init.test_file_append
    
```

```
# 文件目录 
├── init
│   ├── env_init.sls
│   └── test_file_append.sls
└── top.sls

```

## file.append
```
/tmp/abc:
    file.append:
        - text:
            - export ABC=abc
```


## file.recurse
file_rsync:   
   file.recurse:   
     - source: salt://tools   
     - name: /home/tools   
     - user: nobody   
     - group: nobody   
     - dir_mode: 755   
     - file_mode: 644   
     - makedirs: True   
     - backup: minion   
     - include_enpty: True 

## file.managed
```
    file.managed:
        - name: /usr/local/src/pcre-8.39.tar.gz
        - source: salt://pcre/files/pcre-8.39.tar.gz
        - source_hash: {{ checksum }}
        - user: root
        - group: root
        - mode: 755
```

## file.managed {jinja}
```
redis-init-script:
  file.managed:
    - name: /etc/init.d/redis-server
    - template: jinja
    - source: salt://redis/files/redis-init.jinja
    - mode: 0750
    - user: root
    - group: root
    - context:
        conf: /etc/redis/redis.conf
        redis_user: {{ user }}
        exec: {{ bin }}
        pidfile: {{ pidfile }}
    - require:
      - sls: redis.common
```



## cmd.run
```
    cmd.run:
        - name: cd /usr/local/src && tar zxf pcre-8.39.tar.gz && cd pcre-8.39 && ./configure --prefix=/usr/local/pcre && make && make install
        - unless: test -d /usr/local/pcre
        - require:
          - file: pcre-source-install
```

## cmd.wait
```
make-and-install-redis:
  cmd.wait:
    - cwd: {{ root }}/redis-{{ version }}
    - names:
      - make
      - make install
      - cp {{ root }}/redis-{{ version }}/src/redis-cli {{ bin_dir  }}/
      - cp {{ root }}/redis-{{ version }}/src/redis-server {{ bin_dir }}/
    - watch:
      - cmd: get-redis
```

## file.directoy
```
    file.directory:
        - name: /tmp/abc/
        - user: root
        - group: root
        - dir_mode: 755
        - makedirs: True
        - require:
            - cmd: xxxx
            
```

## service.running
```
    service.running:
        - name: nginx
        - enable: True
        - reload: True
        - require:
            - cmd: nginx-init
        - watch:
            - file: /usr/local/nginx/conf/nginx.conf
```


## pkg.installed
```
    pkg.installed:
        - names:
            - openssl-devel
            - swig
            - libjpeg-turbo
            - libjpeg-turbo-devel
            - libpng
            - libpng-devel
            - freetype
            - freetype-devel
            - libxml2
            - libxml2-devel
            - zlib
            - zlib-devel
            - libcurl
            - libcurl-devel
```

## user.present, group.present
```
nobody-user-group:
    group.present:
        - name: nobody
        - gid: 99
    user.present:
        - name: nobody
        - shell: /sbin/nologin
        - uid: 99
        - gid: 99
```






## file.symlink
```
rabbitmq_binary_tool_plugins:
  file.symlink:
    - makedirs: True
    - name: /usr/local/bin/rabbitmq-plugins
    - target: /usr/lib/rabbitmq/bin/rabbitmq-plugins
    - require:
      - pkg: rabbitmq-server
      - file: rabbitmq_binary_tool_env
```


## pkgrepo.managed
```
rabbitmq_repo:
  pkgrepo.managed:
    - humanname: RabbitMQ Packagecloud Repository
    - baseurl: https://packagecloud.io/rabbitmq/rabbitmq-server/el/6/$basearch
    - gpgcheck: 1
    - enabled: True
    - gpgkey: https://packagecloud.io/gpg.key
    - sslverify: 1
    - sslcacert: /etc/pki/tls/certs/ca-bundle.crt
    - require_in:
      - pkg: rabbitmq-server
```


## module.run
```
nginx_user_{{name}}:
  module.run:
    - name: basicauth.adduser
    - user: {{ name }}
    - passwd: {{ user['webauth'] }}
    - path: {{ htauth }}
    - require:
      - pkg: htpasswd
```


## test.check_pillar
```
git-sls-is-pillar-present:
  test.check_pillar:
    - present:
        - git_url
        - git_archive_dir
        - git_resp_base_dir
        - git_tag_name
        - dir_name
```