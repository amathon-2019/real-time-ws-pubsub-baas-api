import json

from websockets import ConnectionClosed

from channel.response_message import ResponseMessage
from db_driver import redis_set_get


async def ws_send_event(app, ws, channel):
    while True:
        try:
            receive_data = json.loads(await ws.recv())

        except ConnectionClosed:
            await channel.leave_channel(app)
            await redis_set_get.del_hash_keys(app, "channels", channel)
            break

        else:
            msg = ResponseMessage(receive_data)
            await channel.send_message(msg)


async def receive_ws_channel(channel, app, ws):
    while True:
        try:
            await channel.receive_message(app, ws)

        except ConnectionClosed:
            break
