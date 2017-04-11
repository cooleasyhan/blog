Date: 2016-09-08
Title: Elasticsearch Logstash 小结
Tags: Linux,Kibana,elasticsearch,logstash,Log
sulg: logstash

## 安装
见之前的文章
建议下载rpm直接安装,一般需要安装jdk, rube

## 参考
[Elasticsearch 权威指南](http://es.xiaoleilu.com/)   
[Logstash 最佳实践](http://udn.yyuap.com/doc/logstash-best-practice-cn/)
[grok debug](http://grokdebug.herokuapp.com/)

## Elasticsearch 类比传统关系型数据库
```
Relational DB -> Databases -> Tables -> Rows -> Columns
Elasticsearch -> Indices   -> Types  -> Documents -> Fields
```

## 整体流程
Elasticsearch 推荐使用redis进行日志中转。所以大体流程如下  
**logfile --> logstash收集 --> redis --> logstash转换,核心为grok进行日志解析 --> Elasticsearch --> kibana展示**


## logstash 收集日志文件配置
```
```

## logstash 收集redis配置
```
```

## Elasticsearch template
对于Elasticsearch其中很重要的一个配置在于template, 而里头最常用的是mapping  

### 新增template
下面是给nginx access log 使用的template, 其中需要注意的是order, Elasticsearch 会根据order 按顺序匹配多个template

```
curl -XPUT localhost:9200/_template/template-logstash-nginx-access -d'
{
    "order": 1,
    "template": "logstash-nginx-access-*",
    "mappings": {
        "nginx-access-log-*": {
            "properties": {
                "remote_addr": {
                    "type": "string"
                },
                "remote_user": {
                    "type": "string"
                },
                "time_local": {
                    "type": "date",
                    "format": "dd/MMM/yyyy:HH:mm:ss Z"
                },
                "request": {
                    "type": "string"
                },
                "status": {
                    "type": "long"
                },
                "body_bytes_sent": {
                    "type": "long"
                },
                "http_user_agent": {
                    "type": "string"
                },
                "http_x_forwarded_for": {
                    "type": "string"
                },
                "request_time": {
                    "type": "double"
                },
                "upstream_response_time": {
                    "type": "string"
                }
            }
        }
    }
}'
```

### 获取现有template
```
curl -XGET localhost:9200/_template | python -m json.tool
```



## 中文分词
比较好的有smartcn和ik,这里用自带的smartcn
```
# /usr/share/elasticsearch/bin/plugin install analysis-smartcn
# service elasticsearch restart
# curl http://127.0.0.1:9200/_analyze/ -d '
{
  "analyzer": "smartcn",
  "text": "联想是全球最大的笔记本厂商"
}'
```
