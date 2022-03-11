from wtforms import Form, IntegerField, TextAreaField, validators


class FibonacciForm(Form):
    from_position = IntegerField(
        label='From', name='from', default=0,
        validators=[validators.NumberRange(min=0)]
    )
    to_position = IntegerField(
        label='To', name='to', default=5,
        validators=[validators.NumberRange(min=0)]
    )
