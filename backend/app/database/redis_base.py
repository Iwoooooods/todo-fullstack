import asyncio
import os
from typing import Optional

import redis.asyncio as redis
from loguru import logger
from redis import Redis


class RedisClient:
    def __init__(self):
        self._url = f"redis://{os.getenv("REDIS_HOST")}:{os.getenv("REDIS_PORT")}/{os.getenv("REDIS_DB")}"
        self.client: Optional[Redis] = None
        logger.info(f"Connected to Redis: {self._url}")

    def init_connection(self):
        pool = redis.ConnectionPool.from_url(self._url)
        self.client = redis.Redis.from_pool(pool)

    async def close_connection(self):
        await self.client.close()


async def get_client():
    return redis_client.client


redis_client = RedisClient()


async def test_connection():
    pong = await redis_client.client.ping()
    print(pong)
    await redis_client.close_connection()


if __name__ == '__main__':
    asyncio.run(test_connection())
