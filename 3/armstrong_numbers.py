import functools


def is_armstrong(number):
    return number == functools.reduce(lambda x, y: x + y, [int(num) ** len(str(number)) for num in str(number)])
