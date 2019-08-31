from dotenv import load_dotenv
from zmq_pubsub import PubSubServer

from channel.channel import Channel

load_dotenv()


async def publish(connection: PubSubServer, channel_name: str, header: str, body: dict):
    await connection.publish(channel_name, header, body)
