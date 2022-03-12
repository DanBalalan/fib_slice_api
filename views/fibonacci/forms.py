from wtforms import Form, IntegerField, SelectField, validators


class FibonacciForm(Form):
    from_arg = IntegerField(
        label='From', name='from_arg', default=0,
        validators=[validators.NumberRange(min=0)]
    )
    to_arg = IntegerField(
        label='To', name='to_arg', default=5,
        validators=[validators.NumberRange(min=0)]
    )
    slice_type = SelectField(
        label='Slice type', name='slice_type', default='pos',
        choices=[('pos', 'By position'), ('val', 'By value')],
    )
