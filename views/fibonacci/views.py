import json
from itertools import count

from flask import request, render_template
from flask.views import MethodView

from utils.fibonacci import fibonacci
from utils.redis_cache import get_cache_key
from utils.redis_client import RedisClient
from settings import CACHE_KEY_PREFIX
from .forms import FibonacciForm


class FibonacciView(MethodView):
    template = 'fibonacci.html'
    max_position_key = f'{CACHE_KEY_PREFIX}:fibonacci_max_cached_position'
    redis_client = RedisClient.get_client()

    def get(self):
        form = FibonacciForm(request.args)
        context = {
            'form': form,
            'result': None,
            'errors': []
        }
        if form.validate():
            context['result'] = {
                'pos': self.__get_by_position(
                    start_pos=form.from_arg.data,
                    stop_pos=form.to_arg.data,
                ),
                'val': self.__get_by_value(
                    min_value=form.from_arg.data,
                    max_value=form.to_arg.data,
                ),
            }[form.slice_type.data]
        else:
            context['errors'].append(form.errors)
        return render_template(self.template, context=context)

    def __get_by_value(self, min_value, max_value):
        if min_value > max_value:
            return []

        max_cached_pos, max_cached_value = self.__get_cached_max_position()
        min_pos = 0
        if min_value > max_cached_value:
            min_pos = max_cached_pos + 1
        elif min_value == max_cached_value:
            min_pos = max_cached_pos
        else:
            min_pos = self.__get_min_position_by_value()  # TODO

        res = []
        for i in count(min_pos, 1):
            fib_by_pos = fibonacci(i)
            if min_value <= fib_by_pos <= max_value:
                res.append(fib_by_pos)
            elif fib_by_pos > max_value:
                break
            else:
                continue
        return res

    def __get_by_position(self, start_pos, stop_pos):
        if start_pos > stop_pos:
            return []

        # Начинаем с максимально возможного значения, попутно заполняя весь недостающий кеш
        cached_max, _ = self.__get_cached_max_position()
        if start_pos > cached_max:
            start_pos = cached_max + 1

        curr_max_pos, curr_max_val = 0, 0
        res = []
        for i in range(start_pos, stop_pos + 1, 1):
            fib_by_pos = fibonacci(i)
            if i >= start_pos:
                res.append(fib_by_pos)
            curr_max_pos, curr_max_val = i, fib_by_pos

        self.__cache_max_position(curr_max_pos, curr_max_val)

        return res

    def __get_min_position_by_value(self, value, cached_max):
        if cached_max[1] >= value:
            pass
        else:
            return cached_max[0]

    def __get_cached_max_position(self):
        cached = self.redis_client.get(self.max_position_key)
        if cached:
            pos, val = json.loads(cached)
        else:
            pos, val = 0, 0
            self.redis_client.set(self.max_position_key, json.dumps((pos, val)))
            fibonacci(pos)  # Создаём кеш от аргументов функции
        return pos, val

    def __cache_max_position(self, pos, val):
        cached_pos, cached_val = self.__get_cached_max_position()
        if cached_pos > pos and cached_val > val:
            return
        self.redis_client.set(self.max_position_key, json.dumps((pos, val)))
