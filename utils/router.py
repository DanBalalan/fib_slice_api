from views import FibonacciView


class Router:

    @staticmethod
    def register_routes(app):
        app.add_url_rule('/fibonacci', view_func=FibonacciView.as_view('fibonacci'), methods=['GET'])

        return app
