from dotenv import dotenv_values
from redis import asyncio as aioredis
import os

config = dotenv_values(".env")
REDIS_URL = os.getenv('REDIS_URL',  config.get('REDIS_URL', "redis://localhost:6379"))

redis = aioredis.from_url(REDIS_URL, encoding="utf8", decode_responses=True)