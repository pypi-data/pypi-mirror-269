from dotenv import dotenv_values
from motor.motor_asyncio import AsyncIOMotorClient
import os

config = dotenv_values(".env")
# 'mongodb://root:example@localhost:27017'
MONGODB_URI = os.getenv('MONGODB_URI',  config.get('MONGODB_URI'))

client = AsyncIOMotorClient(MONGODB_URI)
db = client['tactictrade']