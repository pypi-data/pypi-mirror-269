from threading import Thread

from cacheout import Cache

cache = Cache()


def set_name():
    cache.set("name", "John")


def get_name():
    name = cache.get("name")
    print(name)


def print_test():
    get_name()


Thread(target=set_name).start()

Thread(target=print_test).start()
