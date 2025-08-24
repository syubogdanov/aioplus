from collections.abc import AsyncIterable
from typing import Any, TypeVar, overload

from aioplus.internal.sentinels import Sentinel


T = TypeVar("T")
D = TypeVar("D")


@overload
async def afirst(aiterable: AsyncIterable[T], /) -> T: ...


@overload
async def afirst(aiterable: AsyncIterable[T], /, *, default: D) -> T | D: ...


async def afirst(aiterable: AsyncIterable[Any], /, *, default: Any = Sentinel.UNSET) -> Any:
    """Return the first item of the ``aiterable``.

    Parameters
    ----------
    aiterable : AsyncIterable[T]
        An asynchronous iterable to retrieve the item from.

    default : D, optional
        A default value to return if the iterable is empty.
        If not provided, :obj:`IndexError` will be raised if the iterable is empty.

    Returns
    -------
    T or D
        The first item of ``aiterable`` or the default value.

    Examples
    --------
    >>> aiterable = arange(23)
    >>> await afirst(aiterable)
    0
    """
    if not isinstance(aiterable, AsyncIterable):
        detail = "'aiterable' must be 'AsyncIterable'"
        raise TypeError(detail)

    aiterator = aiter(aiterable)
    value = await anext(aiterator, default)

    if value is Sentinel.UNSET:
        detail = "afirst(): empty iterable"
        raise IndexError(detail) from None

    return value
