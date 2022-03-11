from itertools import count

from flask import request, render_template
from flask.views import MethodView

from utils.fibonacci import fibonacci
from .forms import FibonacciForm


class FibonacciView(MethodView):
    template = 'fibonacci.html'

    def get(self):
        form = FibonacciForm(request.args)
        context = {
            'form': form,
            'result': None,
            'errors': []
        }
        if form.validate():
            context['result'] = {
                'pos': self.__get_by_position(form.from_arg.data, form.to_arg.data),
                'val': self.__get_by_value(form.from_arg.data, form.to_arg.data),
            }[form.slice_type.data]
        else:
            context['errors'].append(form.errors)
        return render_template(self.template, context=context)

    @staticmethod
    def __get_by_value(min_value, max_value):
        if min_value > max_value:
            return []
        res = []
        for i in count(0, 1):
            fib_by_pos = fibonacci(i)
            if min_value <= fib_by_pos <= max_value:
                res.append(fib_by_pos)
            elif fib_by_pos > max_value:
                break
            else:
                continue
        return res

    @staticmethod
    def __get_by_position(start_pos, stop_pos):
        if start_pos > stop_pos:
            return []
        res = []
        # Заполняем с нуля, чтобы избежать ошибки глубины рекурсии при больших стартовых значениях
        for i in range(0, stop_pos + 1, 1):
            fib_by_pos = fibonacci(i)
            if i >= start_pos:
                res.append(fib_by_pos)
        return res

