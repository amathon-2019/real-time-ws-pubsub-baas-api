import asyncio
import os
import time

from dotenv import load_dotenv
from sanic import Sanic
from sanic.request import Request
from sanic.response import json, text
from sanic.websocket import WebSocketProtocol
from zmq_pubsub import PubSubServer

from channel.channel import Channel
from channel.response_message import make_channel_data
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
    return text('index')


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
    channel_list = await redis_set_get.get_hash_all_value(app, 'channels')

    result_data = []
    for item in channel_list:
        channel_name = item
        client_cnt = await app.pub_server.get_channel_client_cnt(channel_name)
        rpm = await app.pub_server.get_channel_request_cnt(channel_name)  # RPM

        result_data.append(make_channel_data(channel_name, client_cnt, rpm))

    return json({"data": result_data})


@app.route("/v1/channel/<channel_name>", methods=['GET'])
async def channel_data(request, channel_name):
    client_cnt = await app.pub_server.get_channel_client_cnt(channel_name)
    rpm = await app.pub_server.get_channel_request_cnt(channel_name)  # RPM

    return text(make_channel_data(channel_name, client_cnt, rpm))


# WebSocketServer
@app.websocket('/channel/<channel_name>/')
async def channel_event(request, ws, channel_name):
    channel = Channel(channel_name)
    await channel.subscribe()

    await redis_set_get.set_hash_data(app, 'channels', channel_name, str(time.time()))

    await channel.client.increase_client_cnt()

    send_task = asyncio.create_task(ws_send_event(ws, channel))
    receive_task = asyncio.create_task(receive_ws_channel(channel, app, ws))
    done, pending = await asyncio.wait(
        [send_task, receive_task],
        return_when=asyncio.FIRST_COMPLETED
    )
    for task in pending:
        task.cancel()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, protocol=WebSocketProtocol)
