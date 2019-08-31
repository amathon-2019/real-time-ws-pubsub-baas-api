from dotenv import load_dotenv

load_dotenv()


async def publish(connection, message):

    await connection.publish('topic', 'header', {'msg': message})
