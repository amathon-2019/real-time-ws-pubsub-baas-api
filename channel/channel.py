import os

from dotenv import load_dotenv
from zmq_pubsub import PubSubClient

from db_driver import redis_set_get

load_dotenv()


class Channel:
    def __init__(self, channel_name):
        self.channel = "channels"
        self.channel_name = channel_name
        self.protocol = None
        self._subscription = None
        self.client = None

    async def set_connection(self):
        self.client = await PubSubClient.create(os.environ['REDIS_URI'])

    async def subscribe(self):
        if self.client is None:
            await self.set_connection()

        self.client.subscribe(f'{self.channel_name}')

    async def receive_message(self, app, ws):
        async for msg in self.client.read_iter():
            print(f'receive {msg}')

    async def get_channel_list(self, app):
        if self.client is None:
            await self.set_connection()

        return redis_set_get.get_all_hash_title(app, self.channel)
