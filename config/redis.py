import json

import redis

from config.settings import get_settings
import logging

logger = logging.getLogger(__name__)

settings = get_settings()

redis_client = redis.Redis.from_url(settings.redis_url, decode_responses=True)


def set_data_redis(key: str, value: str, time: int) -> None:
    try:
        redis_client.set(
            key,
            value,
            ex=time
        )
    except redis.RedisError:
        logger.exception("Failed to connect with Redis")
        return None


def get_data_redis(key: str) -> dict | None:
    try:
        data = redis_client.get(key)
        if data:
            return json.loads(data)
        return None
    except redis.RedisError:
        logger.exception("Failed to connect with Redis")
        return None
