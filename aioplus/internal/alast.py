from collections.abc import AsyncIterable
from typing import Any, TypeVar, overload

from aioplus.internal.atail import atail


T = TypeVar("T")
D = TypeVar("D")


@overload
async def alast(aiterable: AsyncIterable[T], /) -> T: ...


@overload
async def alast(aiterable: AsyncIterable[T], /, *, default: D) -> T | D: ...


async def alast(aiterable: AsyncIterable[Any], /, *, default: Any = ...) -> Any:
    """Return the last item of ``aiterable``.

    Parameters
    ----------
    aiterable : AsyncIterable[T]
        The asynchronous iterable.

    default : D, unset
        A default value to return if the iterable is empty.
        Otherwise, :obj:`IndexError` will be raised.

    Returns
    -------
    T | D
        The last item.

    Examples
    --------
    >>> aiterable = arange(23)
    >>> await alast(aiterable)
    22
    """
    if not isinstance(aiterable, AsyncIterable):
        detail = "'aiterable' must be 'AsyncIterable'"
        raise TypeError(detail)

    aiterator = aiter(atail(aiterable, n=1))
    item = await anext(aiterator, default)

    if item is ...:
        detail = "alast(): empty iterable"
        raise IndexError(detail) from None

    return item
