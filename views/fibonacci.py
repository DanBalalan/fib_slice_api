from itertools import count

from flask.views import MethodView


class FibonacciView(MethodView):

    def get(self):
        # TODO: форму
        return ', '.join(str(i) for i in self.__get_fib())

    def __get_fib(self, min_num=0, max_num=50):
        # TODO: кеш в редис, привести в человеческий вид
        res = []
        for i in count(0):
            curr_fib_num = self.__fib_by_position(i)
            if curr_fib_num > max_num:
                break
            else:
                res.append(curr_fib_num)
        return res

    @staticmethod
    def __fib_by_position(pos):
        if pos in (0, 1):
            return pos
        else:
            return FibonacciView.__fib_by_position(pos - 1) + FibonacciView.__fib_by_position(pos - 2)
