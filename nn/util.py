import asyncio
import functools
from typing import Any, Awaitable, Callable


def click_async(func: Callable[[Any], Any]) -> Callable[[Any], Any]:
    """
    This was taken from this GH issue: https://github.com/pallets/click/issues/2033
    to make it easier to have async support for click functions.

    :param func: a function to be wrapped with async
    :return: returns a wrapped function
    """

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Awaitable[Callable[[Any], Any]]:
        return asyncio.run(func(*args, **kwargs))

    return wrapper
