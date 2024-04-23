import threading

import redis

from stsdk.utils.config import config
from stsdk.utils.log import log


def message_handler(message):
    log.info(f"Received message: {message['data']}")


class RedisUtil:
    def __init__(self):
        host = config.redis_addr
        port = config.redis_port
        password = config.redis_password
        socket_timeout = config.redis_read_timeout
        self.redis = redis.Redis(host=host, port=port, password=password, socket_timeout=socket_timeout)
        self.init_pubsub()

    def init_pubsub(self):
        log.info("init redis pubsub")
        self.pubsub = self.redis.pubsub()
        self.pubsub.subscribe(**{'init-channel': message_handler})
        threading.Thread(target=self.pubsub.run_in_thread, args=()).start()

    def set(self, key, value, ex=None, px=None, nx=False, xx=False):
        log.info(f"set key: {key}, value: {value}")
        self.redis.set(key, value, ex=ex, px=px, nx=nx, xx=xx)

    def get(self, key):
        log.info(f"get key: {key}")
        return self.redis.get(key)

    def batch_insert(self, data):
        log.info(f"batch insert data: {data}")
        pipeline = self.redis.pipeline()
        for key, value in data.items():
            pipeline.set(key, value)
        pipeline.execute()

    def delete(self, *keys):
        log.info(f"delete keys: {keys}")
        return self.redis.delete(*keys)

    def expire(self, key, time):
        log.info(f"expire key: {key}, time: {time}")
        return self.redis.expire(key, time)

    def ttl(self, key):
        log.info(f"ttl key: {key}")
        return self.redis.ttl(key)

    def keys(self, pattern='*'):
        log.info(f"keys pattern: {pattern}")
        return self.redis.keys(pattern)

    def subscribe(self, channel, handler=message_handler):
        log.info(f"subscribe channel: {channel} , handler: {handler}")
        self.pubsub.subscribe(**{channel: handler})

    def publish(self, channel, message):
        log.info(f"publish channel: {channel} , message: {message}")
        self.redis.publish(channel, message)


# redis = RedisUtil()
