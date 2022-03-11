from .redis_cache import redis_cache


@redis_cache
def fibonacci(position):
    if position in (0, 1):
        return position
    else:
        return fibonacci(position - 1) + fibonacci(position - 2)

