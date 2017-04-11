Date: 2016-11-08
Title: 自制pip源
Tags: Python, pip
sulg: pip


## 安装
pip install pip2pi


## 下载文件
```
mkdir /data/pypi
# 编写requirements.txt
pip2tgz /data/pypi -r ./requirements.txt -i http://pypi.douban.com/simple/
# 生成源
dir2pi -N pypi/

# 安装nginx,并指向/data目录
# 使用
pip install pip --upgrade -i http://x.x.x.x:xxxx/pypi/simple --trusted-host x.x.x.x
```


 