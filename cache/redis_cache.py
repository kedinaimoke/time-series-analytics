import redis
import json


class RedisCache:

    def __init__(self):
        self.client = redis.Redis(
            host="localhost",
            port=6379,
            decode_responses=True
        )

        print("Connected to Redis")

    def get(self, key):
        return self.client.get(key)

    def set(self, key, value, ttl=60):
        self.client.set(
            key,
            json.dumps(value),
            ex=ttl
        )
        