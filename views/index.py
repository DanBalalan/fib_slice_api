from flask.views import MethodView


class IndexView(MethodView):

    def get(self):
        return '<p>Index view</p>'
