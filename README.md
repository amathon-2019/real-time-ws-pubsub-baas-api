# real-time-ws-pubsub-baas-api
real-time-ws-pubsub-baas-api


## Stack
sanic      
async, asyncio-redis
## Managing Channel

### HTTP
**Channel List(GET)**
```
http://{hostname}/v1/channel
```
response : 
```json
{
    "data": [
        {
            "channel_name": "a_channel",
            "cnt": 3,
            "rpm": 0
        }
    ]
}
```
**Publish(POST)**
```
http://{hostname}/v1/channel/<channel_name>/publish
```
response:
```json
{
    "status": "ok"
}
```

### WS
**Channel Event**
```
http://{hostname}/channel/{channel_name}/
```
* subscribe
* channel data set redis
* websocket send & receive 
response:
```json
{
    "header":"exchange", 
    "body": {"msg":"ok"}
}
```
