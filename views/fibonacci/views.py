from flask import request, render_template
from flask.views import MethodView

from utils.fibonacci import fibonacci
from.forms import FibonacciForm


class FibonacciView(MethodView):
    template = 'fibonacci.html'

    def get(self):
        form = FibonacciForm(request.args)
        context = {
            'form': form,
            'result': '',
        }
        if form.validate():
            context['result'] = ', '.join(
                str(fibonacci(i)) for i in range(form.from_position.data, form.to_position.data + 1, 1)
            )
        else:
            context['result'] = 'form errors'
        return render_template(self.template, context=context)
