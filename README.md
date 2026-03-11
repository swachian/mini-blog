To run the test:

```
pytest -m "not slow" 

```

or

```
pytest
```


Make a search filter so that the blogs can be queried in this way.

```
http://127.0.0.1:8000/posts/?filters=[{"field":"authorName","operator":"eq","value":"Danny"}]&page=1&pageSize=10

```

create a connector for mongo with kafka

```
    curl -X POST -H "Content-Type: application/json" \
-d '{
  "name": "mongo-posts-source",
  "config": {

    "connector.class": "io.debezium.connector.mongodb.MongoDbConnector",
    "tasks.max": "1",

    "mongodb.connection.string": "mongodb://mongodb-local:27017",

    "database.include.list": "mini_blog",
    "collection.include.list": "mini_blog.posts",

    "topic.prefix": "mongo",

    "snapshot.mode": "initial",

    "transforms": "unwrap,route",

    "transforms.unwrap.type": "io.debezium.connector.mongodb.transforms.ExtractNewDocumentState",

    "transforms.unwrap.drop.tombstones": "true",
    "transforms.unwrap.delete.handling.mode": "rewrite",

    "transforms.route.type": "org.apache.kafka.connect.transforms.RegexRouter",
    "transforms.route.regex": "mongo.mini_blog.posts",
    "transforms.route.replacement": "mini_blog_posts",

    "key.converter": "org.apache.kafka.connect.storage.StringConverter",

    "value.converter": "org.apache.kafka.connect.json.JsonConverter",
    "value.converter.schemas.enable": "false"
  }
}' \
http://localhost:8083/connectors

```

connector如果有问题，可以通过下面的命令查看日志
`docker logs kafka-connect-in-action --tail 200 | grep -i "mongo\|debezium\|error\|exception\|task" --color=always`

另一方面，connector是读取mongodb的binlog的，而这个log只有在replication打开的情况下才有，所以需要重新调整mongo的docker,打开replication.这样才能实际启动上面的connector


如果遇到Dockerfile里要从外部下载的东西，可以通过这个命令传递代理信息给build服务.  
`docker-compose build --build-arg HTTPS_PROXY=http://127.0.0.1:7897`

用下面的指令可以测试：
```
curl -X POST "localhost:9200/_analyze?pretty" -H 'Content-Type: application/json' -d'
{
  "analyzer": "ik_max_word",
  "text": "如果你厌倦了伦敦，你就厌倦了生活。欧洲最好的城市是罗马，当然是罗马。"
}'

可以得到下面这样的响应：
{
  "tokens" : [
    {
      "token" : "如果",
      "start_offset" : 0,
      "end_offset" : 2,
      "type" : "CN_WORD",
      "position" : 0
    },
    {
      "token" : "你",
      "start_offset" : 2,
      "end_offset" : 3,
      "type" : "CN_CHAR",
      "position" : 1
    },
    {
      "token" : "厌倦",
      "start_offset" : 3,
      "end_offset" : 5,
      "type" : "CN_WORD",
      "position" : 2
    },
    {
      "token" : "了",
      "start_offset" : 5,
      "end_offset" : 6,
      "type" : "CN_CHAR",
      "position" : 3
    },
    {
      "token" : "伦敦",
      "start_offset" : 6,
      "end_offset" : 8,
      "type" : "CN_WORD",
      "position" : 4
    },
    {
      "token" : "你",
      "start_offset" : 9,
      "end_offset" : 10,
      "type" : "CN_CHAR",
      "position" : 5
    },
    {
      "token" : "就",
      "start_offset" : 10,
      "end_offset" : 11,
      "type" : "CN_CHAR",
      "position" : 6
    },
    {
      "token" : "厌倦",
      "start_offset" : 11,
      "end_offset" : 13,
      "type" : "CN_WORD",
      "position" : 7
    },
    {
      "token" : "了",
      "start_offset" : 13,
      "end_offset" : 14,
      "type" : "CN_CHAR",
      "position" : 8
    },
    {
      "token" : "生活",
      "start_offset" : 14,
      "end_offset" : 16,
      "type" : "CN_WORD",
      "position" : 9
    },
    {
      "token" : "欧洲",
      "start_offset" : 17,
      "end_offset" : 19,
      "type" : "CN_WORD",
      "position" : 10
    },
    {
      "token" : "最好",
      "start_offset" : 19,
      "end_offset" : 21,
      "type" : "CN_WORD",
      "position" : 11
    },
    {
      "token" : "的",
      "start_offset" : 21,
      "end_offset" : 22,
      "type" : "CN_CHAR",
      "position" : 12
    },
    {
      "token" : "城市",
      "start_offset" : 22,
      "end_offset" : 24,
      "type" : "CN_WORD",
      "position" : 13
    },
    {
      "token" : "是",
      "start_offset" : 24,
      "end_offset" : 25,
      "type" : "CN_CHAR",
      "position" : 14
    },
    {
      "token" : "罗马",
      "start_offset" : 25,
      "end_offset" : 27,
      "type" : "CN_WORD",
      "position" : 15
    },
    {
      "token" : "当然是",
      "start_offset" : 28,
      "end_offset" : 31,
      "type" : "CN_WORD",
      "position" : 16
    },
    {
      "token" : "当然",
      "start_offset" : 28,
      "end_offset" : 30,
      "type" : "CN_WORD",
      "position" : 17
    },
    {
      "token" : "是",
      "start_offset" : 30,
      "end_offset" : 31,
      "type" : "CN_CHAR",
      "position" : 18
    },
    {
      "token" : "罗马",
      "start_offset" : 31,
      "end_offset" : 33,
      "type" : "CN_WORD",
      "position" : 19
    }
  ]
```

给es定义schema mapping和分词的要求 

```
# 创建索引并指定中文分析器
curl -X PUT "localhost:9200/mini_blog_posts" -H 'Content-Type: application/json' -d'
{
  "mappings": {
    "properties": {
      "title": {
        "type": "text",
        "analyzer": "ik_max_word",      
        "search_analyzer": "ik_smart"  
      },
      "content": {
        "type": "text",
        "analyzer": "ik_max_word",
        "search_analyzer": "ik_smart"
      },
      "author_name": {
        "type": "keyword"               
      },
      "tags": {
        "type": "keyword"  
      },
      "created_at": {
        "type": "date"
      }
    }
  }
}'


```


```
curl -X DELETE http://localhost:8083/connectors/es-posts-sink

curl -X POST http://localhost:8083/connectors \
  -H "Content-Type: application/json" \
  -d '{
    "name": "es-posts-sink",
    "config": {
      "connector.class": "io.confluent.connect.elasticsearch.ElasticsearchSinkConnector",
      "tasks.max": "1",
      "topics": "mini_blog_posts",
      "connection.url": "http://elasticsearch:9200",
      "key.ignore": "true",
      "schema.ignore": "true",
      "behavior.on.null.values": "delete",
      
      "transforms": "unwrap,extractAfter",
      "transforms.unwrap.type": "io.debezium.transforms.ExtractNewRecordState",
      "transforms.unwrap.drop.tombstones": "true",
      
      "transforms.extractAfter.type": "org.apache.kafka.connect.transforms.ExtractField$Value",
      "transforms.extractAfter.field": "after",
      
      "value.converter": "org.apache.kafka.connect.json.JsonConverter",
      "value.converter.schemas.enable": "false"
    }
  }'
```

有一个坑的地方，kafka的es sink 15.xx目前也仅能支持es 8.x。如果使用9.x的版本，sink就会报400错误。