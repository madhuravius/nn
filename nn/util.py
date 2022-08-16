import asyncio
import functools


def click_async(func):
    """
    This was taken from this GH issue: https://github.com/pallets/click/issues/2033
    to make it easier to have async support for click functions.

    :param func: a function to be wrapped with async
    :return: returns a wrapped function
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return asyncio.run(func(*args, **kwargs))

    return wrapper
