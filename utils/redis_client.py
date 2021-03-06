from redis import Redis

from settings import REDIS_DEFAULT_PORT, REDIS_DEFAULT_HOST, REDIS_DEFAULT_DB
from utils.singleton import Singleton


class RedisClient(metaclass=Singleton):

    @staticmethod
    def get_client(host=REDIS_DEFAULT_HOST, port=REDIS_DEFAULT_PORT, db=REDIS_DEFAULT_DB, decode_responses=True):
        return Redis(host=host, port=port, db=db, decode_responses=decode_responses)
