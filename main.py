import asyncio
import os
import time

from dotenv import load_dotenv
from sanic import Sanic
from sanic.request import Request
from sanic.response import json
from sanic.websocket import WebSocketProtocol
from zmq_pubsub import PubSubServer

from channel.channel import Channel
from db_driver import redis_set_get
from ws_handler.ws_send_receive import ws_send_event, receive_ws_channel

load_dotenv()

app = Sanic(__name__)
app.pub_server: PubSubServer


@app.listener('before_server_start')
async def setup(app, loop):
    app.conn = await redis_set_get.create_connection_pool()
    app.pub_server = await PubSubServer.create(os.environ['REDIS_URI'])
    loop.create_task(app.pub_server.run_forever())


@app.listener('after_server_stop')
async def close_db(app, loop):
    await app.close()


# HTTP GET
@app.route("/", methods=['GET'])
async def main(request):
    message = {"test": "a"}
    await app.pub_server.publish('b', 'exchange', message)
    return json({"data": "1"})


@app.route("/v1/channel/<channel_name>/publish", methods=['POST'])
async def publish(request: Request, channel_name):
    response: dict = request.json
    if response:
        if response.get('header') and response.get('body'):
            await app.pub_server.publish(channel_name, response.get('header'), response.get('body'))
            return json({"status": "ok"})

    return json({"status": "fail"}, 403)


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
    except Exception:
        message = 'FAIL'
    return json({"message": message})


@app.route("/v1/channel/<channel_name>/delete", methods=["POST"])
async def unsubscribe_channel(request, channel_name):
    # deleted_sign
    del_result = await redis_set_get.del_hash_keys(app, 'channels', channel_name)

    if del_result != 0:
        result_message = "SUCCESS"
    else:
        result_message = "FAIL"

    return json({"message": result_message})


# WebSocketServer
@app.websocket('/channel/<channel_name>/')
async def channel_event(request, ws, channel_name):
    msg = "test"

    channel = Channel(channel_name)
    await channel.subscribe()
    send_task = asyncio.create_task(ws_send_event(app, ws, channel, msg))
    receive_task = asyncio.create_task(receive_ws_channel(channel, app, ws))
    done, pending = await asyncio.wait(
        [send_task, receive_task],
        return_when=asyncio.FIRST_COMPLETED
    )
    for task in pending:
        task.cancel()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, protocol=WebSocketProtocol)
