from collections.abc import AsyncIterable
from typing import Any, TypeVar, overload

from aioplus.internal.aenumerate import aenumerate


T = TypeVar("T")
D = TypeVar("D")


@overload
async def anth(aiterable: AsyncIterable[T], /, *, n: int) -> T: ...


@overload
async def anth(aiterable: AsyncIterable[T], /, *, n: int, default: D) -> T | D: ...


async def anth(aiterable: AsyncIterable[Any], /, *, n: int, default: Any = ...) -> Any:
    """Return the nth item of ``aiterable``.

    Parameters
    ----------
    aiterable : AsyncIterable[T]
        The asynchronous iterable.

    n : int
        The index.

    default : D, unset
        A default value to return if the nth item does not exist. Otherwise, :obj:`IndexError` will
        be raised.

    Returns
    -------
    T | D
        The nth item.

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

    async for index, item in aenumerate(aiterable):
        if index == n:
            return item

    if default is ...:
        detail = "'aiterable[n]' does not exist"
        raise IndexError(detail)

    return default
