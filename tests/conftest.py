import pytest
from redis import Redis
import settings
from app import app as test_app
from utils.router import Router

test_app = Router.register_routes(test_app)


@pytest.fixture()
def app():

    test_app.testing = True

    # other setup can go here

    yield test_app

    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.fixture()
def redis_client():
    return Redis(
        host=settings.REDIS_DEFAULT_HOST,
        port=settings.REDIS_DEFAULT_PORT,
        db=settings.REDIS_DEFAULT_DB,
        decode_responses=True
    )
