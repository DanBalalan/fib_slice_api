import os

from flask import Flask

from utils.router import Router
from utils.constants import ENV_NAME_DEPLOY_TYPE, ENV_NAME_HOST, \
    ENV_NAME_PORT, ENV_VALUE_DEV, DEFAULT_HOST, DEFAULT_PORT


app = Flask(__name__)


if __name__ == '__main__':
    app = Router().register_routes(app)
    app.run(
        debug=os.getenv(ENV_NAME_DEPLOY_TYPE, ENV_VALUE_DEV) == ENV_VALUE_DEV,
        host=os.getenv(ENV_NAME_HOST, DEFAULT_HOST),
        port=os.getenv(ENV_NAME_PORT, DEFAULT_PORT)
    )
