import asyncio
import time

import asyncio_redis
from sanic import Sanic
from sanic.response import json
from sanic.websocket import WebSocketProtocol

from channel.channel import Channel
from db_driver import redis_set_get
from ws_handler.ws_send_receive import ws_send_event, receive_ws_channel

app = Sanic(__name__)
app: asyncio_redis.Pool


@app.listener('before_server_start')
async def setup(app, loop):
    app.conn = await redis_set_get.create_connection_pool()


@app.listener('after_server_stop')
async def close_db(app, loop):
    await app.close()

# HTTP GET
@app.route("/", methods=['GET'])
async def main(request):
    return json({"hello": "main"})


@app.route("/v1/channel", methods=['GET'])
async def channel_list(request):
    data = await redis_set_get.get_hash_all_value(app, 'channels')
    return json({"data": data})


# HTTP POST
@app.route("/v1/channel/<channel_name>", methods=["POST"])
async def subscribe_channel(request, channel_name):
    channel_title = request.form.get('channel_name')

    try:
        await redis_set_get.set_hash_data(app, 'channels', channel_title, str(time.time()))
        message = 'SUCCESS'
    except Exception as e:
        print(e)
        message = 'FAIL'
    return json({
        "message": message
    })


@app.route("/v1/channel/<channel_name>/delete", methods=["POST"])
async def unsubscribe_channel(request, channel_name):
    # message = response_message.ResponseMessage.make_deleted_sign(channel)
    # await zmq_pub_sub.send_message(channel, message)
    del_result = await redis_set_get.del_hash_keys(app, 'channels', channel_name)

    # FIXME: Exception 처리가 좋을듯
    if del_result != 0:
        return json({"message": "SUCCESS"})
    else:
        return json({"message": "FAIL"})


# WebSocketServer
@app.websocket('/channel/<channel_name>/')
async def room_chat(request, ws, channel_name):
    channel = Channel(channel_name)

    await channel.join_channel(app)

    send_task = asyncio.create_task(ws_send_event(app, ws, channel))
    receive_task = asyncio.create_task(receive_ws_channel(channel, app, ws))
    done, pending = await asyncio.wait(
        [send_task, receive_task],
        return_when=asyncio.FIRST_COMPLETED
    )
    for task in pending:
        task.cancel()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, protocol=WebSocketProtocol)
