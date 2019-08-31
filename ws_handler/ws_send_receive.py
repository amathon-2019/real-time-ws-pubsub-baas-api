import json

from websockets import ConnectionClosed, WebSocketCommonProtocol

from channel.channel import Channel
from db_driver import redis_set_get


async def ws_send_event(ws, channel: Channel):
    async for event in channel.client.read_iter():
        await ws.send(json.dumps(event.body))


async def receive_ws_channel(channel: Channel, app, ws: WebSocketCommonProtocol):
    while True:
        try:
            msg = await ws.recv()
            print(f'ws recv: {msg}')

            try:
                request: dict = json.loads(msg)
                if request.get('header') and request.get('body'):
                    await app.pub_server.publish(channel.channel_name, request.get('header'), request.get('body'))
            except json.JSONDecodeError:
                pass

        except ConnectionClosed:
            await channel.client.decrease_client_cnt()
            await redis_set_get.del_hash_keys(app, 'channels', [channel.channel_name])
            break
