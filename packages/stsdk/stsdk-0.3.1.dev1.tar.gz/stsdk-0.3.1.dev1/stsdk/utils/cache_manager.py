from collections import deque

from cacheout import Cache


class CacheManager:
    def __init__(self):
        self.cache = Cache()

    def get_cache_queue(self, key):
        return self.cache.get(key)

    def set_cache_queue(self, key, value):
        queue = self.get_cache_queue(key)
        if queue is None:
            queue = deque(maxlen=10)
        queue.append(value)
        self.cache.set(key, queue)

    def get_cache(self, key):
        return self.cache.get(key)

    def set_cache(self, key, value):
        self.cache.set(key, value)

    # 谨慎使用，会清除所有缓存
    def clear_cache(self):
        self.cache.clear()

    def delete_cache(self, key):
        self.cache.delete(key)

    def has_cache(self, key):
        return self.cache.has(key)


cache_manager = CacheManager()
