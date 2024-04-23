import functools


def divide(*args: [int]):
    return functools.reduce(lambda a, b: a / b, args)
