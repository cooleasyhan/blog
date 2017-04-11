Date: 2016-11-08
Title: pip2pi
Tags: Python, pip
sulg: pip


##  安装
pip install pip2pi


## 生成
```
mkdir /data/pypi
# requirements.txt
pip2tgz /data/pypi -r ./requirements.txt -i http://pypi.douban.com/simple/
# 启动服务
dir2pi -N pypi/

# 使用
pip install pip --upgrade -i http://x.x.x.x:xxxx/pypi/simple --trusted-host x.x.x.x
```


 