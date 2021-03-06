from flask import request, render_template
from flask.views import MethodView

from utils.fibonacci import get_by_position_range, get_by_value_range
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
                'pos': get_by_position_range(
                    start_pos=form.from_arg.data,
                    stop_pos=form.to_arg.data,
                ),
                'val': get_by_value_range(
                    min_value=form.from_arg.data,
                    max_value=form.to_arg.data,
                ),
            }[form.slice_type.data]
        else:
            context['errors'].append(form.errors)
        return render_template(self.template, context=context)
