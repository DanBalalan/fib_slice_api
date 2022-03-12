import json
from functools import wraps

from utils.redis_client import RedisClient
from settings import CACHE_KEY_PREFIX


def get_cache_key(func, args, kwargs):
    return f'{CACHE_KEY_PREFIX}:' \
           f'{func.__name__}:' \
           f'{"-".join(str(i) for i in args) if args else "no_args"}:' \
           f'{"-".join(f"{str(k)}_{str(kwargs[k])}" for k in sorted(kwargs)) if kwargs else "no_kwargs"}'


def redis_cache(func):
    redis_client = RedisClient.get_client()

    @wraps(func)
    def wrapper(*args, **kwargs):
        key = get_cache_key(func, args, kwargs)

        result = redis_client.get(key)
        if result:
            result = json.loads(result)
        else:
            result = func(*args, **kwargs)
            redis_client.set(key, json.dumps(result))

        return result
    return wrapper
