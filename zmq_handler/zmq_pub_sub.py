import asyncio
import os
from dotenv import load_dotenv
from zmq_pubsub import PubSubServer

load_dotenv()


async def publish(connection):

    await connection.publish('topic', 'header', {'msg': 'hello'})
