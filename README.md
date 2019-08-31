# real-time-ws-pubsub-baas-api
real-time-ws-pubsub-baas-api by team16


## Stack
sanic    
aiozmq,async-redis
## Managing Channel

HTTP
```
http://{hostname}/v1/channel/{channel_name}/subscribers
```

WS
``````
## Channel Format
```json
 {
    "channel": "example",
    "header": "",
    "body": ""
  }
```
