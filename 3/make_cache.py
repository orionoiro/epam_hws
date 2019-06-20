import time
import functools


def request(*args):
    return args[0], {'data': args[2], 'last_usage': args[1]}


def make_cache(timeout=0):
    def decorator(func):
        cache = {}

        @functools.wraps(func)
        def wrapper(*args):
            try:
                if args[1] - cache[args[0]]['last_usage'] >= timeout:
                    del cache[args[0]]
                return cache[args[0]]['data'] == args[2]
            except KeyError:
                response = request(*args)
                if (args[0], args[2]) == (response[0], response[1]['data']):
                    cache[response[0]] = response[1]
                    return True
                return False
        return wrapper
    return decorator


@make_cache(timeout=30)
def slow_function(uid, current_time, hashed_data):
    """uid - user id
       hashed_data - hashed biometrics information about user

       If uid not in cache, sends request to database server
       and compares input with response.
       Decorator argument sets amount of caching time
       for each user.
       True - access granted
       False - access denied"""


slow_function(5, time.time(), '79725fa4d2302d2cc550b733fa3e817aa88ce28dafa90833b8503cc769f2e7c1#')
time.sleep(5)
slow_function(5, time.time(), '79725fa4d2302d2cc550b733fa3e817aa88ce28dafa90833b8503cc769f2e7c1#')
time.sleep(30)
slow_function(5, time.time(), '79725fa4d2302d2cc550b733fa3e817aa88ce28dafa90833b8503cc769f2e7c1#')
slow_function(6, time.time(), '60a7861aa75fee46f65d06782f0ab4e6a7339285ef99bb9778c748bb0968c0b5#')
