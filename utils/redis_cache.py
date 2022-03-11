import json
from functools import wraps

from redis import Redis

from settings import REDIS_DEFAULT_PORT, REDIS_DEFAULT_HOST, REDIS_DEFAULT_DB, CACHE_KEY_PREFIX


def redis_cache(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        key = f'{CACHE_KEY_PREFIX}:' \
              f'{func.__name__}:' \
              f'{"-".join(str(i) for i in args) if args else "no_args"}:' \
              f'{"-".join(f"{str(k)}_{str(kwargs[k])}" for k in sorted(kwargs)) if kwargs else "no_kwargs"}'
        with Redis(host=REDIS_DEFAULT_HOST, port=REDIS_DEFAULT_PORT, db=REDIS_DEFAULT_DB, decode_responses=True) as r:
            result = r.get(key)

            if result:
                result = json.loads(result)
                print(f'got from cache key: {key}\nresult: {result}')
            else:
                result = func(*args, **kwargs)
                print(f'no cache key: {key}\nsaving: {result}')
                r.set(key, json.dumps(result))

        return result
    return wrapper

