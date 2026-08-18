import json

import redis

redis_client = redis.Redis(
    host="redis",
    port=6379,
    decode_responses=True,
)

def set_data_redis(key: str, value, time: int) -> None:
    redis_client.set(
        key,
        value,
        ex=time
    )

def get_data_redis(key: str):
    data = redis_client.get(key)
    if data:
        return json.loads(data)
    return None