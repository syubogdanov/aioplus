from collections.abc import AsyncIterable
from typing import Any, SupportsIndex, TypeVar, overload

from aioplus.internal.aenumerate import aenumerate
from aioplus.internal.coercions import to_async_iterable, to_non_negative_int
from aioplus.internal.sentinels import Sentinel


T = TypeVar("T")
D = TypeVar("D")


@overload
async def anth(aiterable: AsyncIterable[T], /, *, n: SupportsIndex) -> T: ...


@overload
async def anth(aiterable: AsyncIterable[T], /, *, n: SupportsIndex, default: D) -> T | D: ...


async def anth(
    aiterable: AsyncIterable[Any],
    /,
    *,
    n: SupportsIndex,
    default: Any = Sentinel.UNSET,
) -> Any:
    """Return the nth item or a default value.

    Parameters
    ----------
    aiterable : AsyncIterable[T]
        An asynchronous iterable to retrieve the nth item from.

    n : SupportsIndex
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
    aiterable = to_async_iterable(aiterable, variable_name="aiterable")
    n = to_non_negative_int(n, variable_name="n")

    async for index, value in aenumerate(aiterable):
        if index == n:
            return value

    if default is Sentinel.UNSET:
        detail = "'aiterable[n]' does not exist"
        raise IndexError(detail)

    return default
