import redis
import json
from urllib.parse import urlparse


class RedisSessionStore:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__initialized = False
        return cls._instance

    def __init__(self, url='redis://localhost:6379/0'):
        if self.__initialized: return
        self.__initialized = True
        parsed_url = urlparse(url)
        print(f'Connecting to Redis: {parsed_url.hostname}:{parsed_url.port}')
        self.redis = redis.Redis(
            host=parsed_url.hostname,
            port=parsed_url.port,
            username=parsed_url.username,
            password=parsed_url.password
        )
        print('Connected to Redis')

    def set(self, key, value):
        self.redis.set(key, json.dumps(value))

    def get(self, key):
        return json.loads(self.redis.get(key))

    def delete(self, key):
        self.redis.delete(key)



