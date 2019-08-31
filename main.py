from sanic import Sanic
from sanic.response import json
from sanic.websocket import WebSocketProtocol

from channel import response_message
from db_driver import redis_set_get
import asyncio_redis

app = Sanic(__name__)
app: asyncio_redis.Pool


@app.listener('before_server_start')
async def setup(app, loop):
    app.conn = await redis_set_get.create_connection_pool()


@app.listener('after_server_stop')
async def close_db(app, loop):
    await app.close()


# @app.middleware('response')
# async def allow_cross_site(request, response):
#     response.headers["Access-Control-Allow-Origin"] = "http://localhost:8080"
#     response.headers["Access-Control-Allow-Credentials"] = "true"
#     # response.headers["Access-Control-Allow-Headers"] = "*"


# HTTP
@app.route("/", methods=['GET'])
async def main(request):
    return json({"hello": "main"})


@app.route("/v1/channel", methods=['GET'])
async def channel_list(request):
    data = await redis_set_get.get_hash_all_value(app, 'channels')
    return json({"data": data})


# HTTP POST
@app.route("/v1/channel/<channel>", methods=["POST"])
async def subscribe_channel(request, channel):
    channel_title = request.form.get('channel')

    try:
        await redis_set_get.set_hash_data(app, 'channels', channel, "1")
        message = 'SUCCESS'
    except Exception as e:
        print(e)
        message = 'FAIL'
    return json({
        "message": message
    })


@app.route("/v1/channel/<channel>/delete", methods=["POST"])
async def unsubscribe_channel(request, channel):
    # message = response_message.ResponseMessage.make_deleted_sign(channel)
    # await zmq_pub_sub.send_message(channel, message)
    del_result = await redis_set_get.del_hash_keys(app, 'channels', [channel])
    print(del_result)

    # FIXME: Exception 처리가 좋을듯
    if del_result != 0:
        return json({"message": "SUCCESS"})
    else:
        return json({"message": "FAIL"})


# WS


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, protocol=WebSocketProtocol)
