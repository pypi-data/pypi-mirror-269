import functools


def multiply(*args: [int]):
    return functools.reduce(lambda a, b: a * b, args)
