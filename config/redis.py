import json

import redis

from config.settings import get_settings

settings = get_settings()

redis_client = redis.Redis.from_url(settings.redis_url, decode_responses=True)


def set_data_redis(key: str, value: str, time: int) -> None:
    redis_client.set(
        key,
        value,
        ex=time
    )


def get_data_redis(key: str) -> dict | None:
    data = redis_client.get(key)
    if data:
        return json.loads(data)
    return None
