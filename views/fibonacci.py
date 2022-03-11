from flask import request
from flask.views import MethodView

from utils.fibonacci import fibonacci


class FibonacciView(MethodView):

    def get(self):
        from_ = int(request.args.get('from', 0))
        to_ = int(request.args.get('to', 0))
        if from_ > to_ or from_ < 0 or to_ < 0:
            return ''
        return ', '.join(str(fibonacci(i)) for i in range(from_, to_ + 1, 1))
