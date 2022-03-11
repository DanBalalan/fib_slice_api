from itertools import count

from flask.views import MethodView

from utils.fibonacci import fibonacci


class FibonacciView(MethodView):

    def get(self):
        # TODO: форму
        return ', '.join(str(i) for i in self.__get_fib())

    def __get_fib(self, min_num=0, max_num=50):
        res = []
        for i in count(0):
            curr_fib_num = fibonacci(position=i)
            if curr_fib_num > max_num:
                break
            else:
                res.append(curr_fib_num)
        return res
