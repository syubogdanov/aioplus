from collections.abc import AsyncIterable
from typing import Any, TypeVar, overload

from aioplus.internal.aenumerate import aenumerate
from aioplus.internal.sentinels import Sentinel


T = TypeVar("T")
D = TypeVar("D")


@overload
async def anth(aiterable: AsyncIterable[T], /, *, n: int) -> T: ...


@overload
async def anth(aiterable: AsyncIterable[T], /, *, n: int, default: D) -> T | D: ...


async def anth(aiterable: AsyncIterable[Any], /, *, n: int, default: Any = Sentinel.UNSET) -> Any:
    """Return the nth item or a default value.

    Parameters
    ----------
    aiterable : AsyncIterable[T]
        An asynchronous iterable to retrieve the nth item from.

    n : int
        The index of the item to retrieve, starting from 0.

    default : D, optional
        A default value to return if the nth item does not exist.
        If not provided, :obj:`IndexError` will be raised if the nth item is not found.

    Returns
    -------
    T or D
        The nth item or the default value.

    Examples
    --------
    >>> aiterable = arange(23)
    >>> await anth(aiterable, n=4)
    4
    """
    if not isinstance(aiterable, AsyncIterable):
        detail = "'aiterable' must be 'AsyncIterable'"
        raise TypeError(detail)

    if not isinstance(n, int):
        detail = "'n' must be 'int'"
        raise TypeError(detail)

    if n < 0:
        detail = "'n' must be non-negative"
        raise ValueError(detail)

    async for index, value in aenumerate(aiterable):
        if index == n:
            return value

    if default is Sentinel.UNSET:
        detail = "'aiterable[n]' does not exist"
        raise IndexError(detail)

    return default
