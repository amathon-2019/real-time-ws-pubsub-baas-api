# real-time-ws-pubsub-baas-api
real-time-ws-pubsub-baas-api by team16


## Stack
sanic      
aiozmq, asyncio-redis
## Managing Channel

### HTTP
**Channel List**
```
http://{hostname}/v1/channel
```
**Subscribe Channel**
```
http://{hostname}/v1/channel/{channel_name}/
```
**UnSubscribe Channel**
```
http://{hostname}/v1/channel/{channel_name}/delete
```
### WS
**Channel Event**
```
http://{hostname}/channel/{channel_name}/
```

## Channel Format
```json
 {
    "channel": "example",
    "header": "",
    "body": ""
  }
```
