import json
from itertools import count

from settings import CACHE_KEY_PREFIX
from .binary_search import binary_search_nearest
from .redis_cache import redis_cache
from .redis_client import RedisClient


MAX_CACHED_KEY = f'{CACHE_KEY_PREFIX}:fibonacci:max_cached'


@redis_cache
def fibonacci(position):
    if position in (0, 1):
        return position
    else:
        return fibonacci(position - 1) + fibonacci(position - 2)


def get_by_value_range(min_value, max_value):
    if min_value > max_value:
        return []

    # Начинаем с максимально возможного значения, попутно заполняя весь недостающий кеш
    # (предполагая, что существующий кеш непрерывный и целостный)
    max_cached_pos, max_cached_value = get_max_cached()
    if min_value > max_cached_value:
        min_pos = max_cached_pos + 1
    elif min_value == max_cached_value:
        min_pos = max_cached_pos
    else:  # min_value < max_cached_value
        positions_sequence = [i for i in range(0, max_cached_pos, 1)]
        min_pos, exact = binary_search_nearest(positions_sequence, min_value, fibonacci)
        if not exact and min_pos > 0:
            min_pos -= 1

    curr_max_pos, curr_max_val = 0, 0
    res = []
    for i in count(min_pos, 1):
        fib_by_pos = fibonacci(i)
        curr_max_pos, curr_max_val = i, fib_by_pos
        if min_value <= fib_by_pos <= max_value:
            res.append(fib_by_pos)
        elif fib_by_pos > max_value:
            break
        else:
            continue

    set_max_cached(curr_max_pos, curr_max_val)
    return res


def get_by_position_range(start_pos, stop_pos):
    if start_pos > stop_pos:
        return []

    # Начинаем с максимально возможного значения, попутно заполняя весь недостающий кеш
    # (предполагая, что существующий кеш непрерывный и целостный)
    # start_iter_pos - для заполнения кеша при отсутсвии какой-либо части его диапазона
    # start_pos - начальная искомая позиция, значение в которой отдаётся наружу
    cached_max, _ = get_max_cached()
    start_iter_pos = start_pos
    if start_pos > cached_max:
        start_iter_pos = cached_max + 1

    curr_max_pos, curr_max_val = 0, 0
    res = []
    for i in range(start_iter_pos, stop_pos + 1, 1):
        fib_by_pos = fibonacci(i)
        if i >= start_pos:
            res.append(fib_by_pos)
        curr_max_pos, curr_max_val = i, fib_by_pos

    set_max_cached(curr_max_pos, curr_max_val)
    return res


def get_max_cached():
    cached = RedisClient.get_client().get(MAX_CACHED_KEY)
    if cached:
        pos, val = json.loads(cached)
    else:
        pos, val = 0, 0
        RedisClient.get_client().set(MAX_CACHED_KEY, json.dumps((pos, val)))
        fibonacci(pos)  # Создаём кеш от аргументов функции
    return pos, val


def set_max_cached(pos, val):
    cached_pos, cached_val = get_max_cached()
    if cached_pos > pos and cached_val > val:
        return
    RedisClient.get_client().set(MAX_CACHED_KEY, json.dumps((pos, val)))
