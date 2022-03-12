import json
from utils.redis_cache import get_cache_key, redis_cache


class TestRedisCache:
    __test_func_call_count = 0

    @redis_cache
    def __test_func(self, argument='default'):
        self.__test_func_call_count += 1
        return argument

    def __call_cached(self, redis_client, args, kwargs, reset_call_count=True, num_calls=5, cleanup=True):
        if reset_call_count:
            self.__test_func_call_count = 0

        key = get_cache_key(self.__test_func, (self,) + args, kwargs)
        for _ in range(num_calls):
            res = self.__test_func(*args, **kwargs)

        assert self.__test_func_call_count == 1
        try:
            assert len(redis_client.keys(f'*:{self.__test_func.__name__}:*{self}*')) == 1
            assert json.loads(redis_client.get(key)) == res
        finally:
            if cleanup:
                redis_client.delete(key)
                assert not [k for k in redis_client.keys(f'*:{self.__test_func.__name__}:*{self}*')]

    def test_connection(self, redis_client):
        redis_client.keys()

    def test_cache_args(self, redis_client):
        self.__call_cached(redis_client, (1,), {})

    def test_cache_kwargs(self, redis_client):
        self.__call_cached(redis_client, (), {'argument': 'foo'})

    def test_cache_default_value(self, redis_client):
        self.__call_cached(redis_client, (), {})
