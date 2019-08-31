import time

from db_driver import redis_set_get
from zmq_handler import zmq_pub_sub


# zmq_pub_sub 미 적용

class Channel:
    def __init__(self, channel_name):
        self.channel = "channels"
        self.channel_name = channel_name
        self.is_connected = False
        self.connection = None
        self.protocol = None
        self._subscription = None

    async def _connect(self):
        self.connection = await zmq_pub_sub.create_connection_pool()
        self.is_connected = True

    async def join_channel(self, app):
        if not self.is_connected:
            await self._connect()

        await redis_set_get.set_hash_data(app, self.channel, self.channel_name, str(time.time()))
        self._subscription = await zmq_pub_sub.subscribe_channel(self.connection, self.channel)

    async def leave_channel(self, app, channel):
        if not self.is_connected:
            await self._connect()

        await zmq_pub_sub.unsubscibe_channel(self._subscription, self.channel_name)
        await redis_set_get.del_hash_keys(app, self.channel, self.channel_name)

    async def send_message(self, message):
        if not self.is_connected:
            await self._connect()

        return await zmq_pub_sub.send_message(self.channel_name, message)

    async def receive_message(self, app, ws):
        if not self.is_connected:
            await self._connect()

        while True:
            try:
                message = await zmq_pub_sub.receive_message(self._subscription)
                await ws.send(str(message.value))
            except ConnectionError:
                await zmq_pub_sub.unsubscibe_channel(self._subscription, self.channel_name)
                await redis_set_get.del_hash_keys(app, self.channel, self.channel_name)

    async def get_channel_list(self, app):
        if not self.is_connected:
            await self.connection()

        return redis_set_get.get_all_hash_title(app, self.channel)
