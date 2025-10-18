from collections.abc import AsyncIterable
from typing import Any, TypeVar, overload


T = TypeVar("T")
D = TypeVar("D")


@overload
async def afirst(aiterable: AsyncIterable[T], /) -> T: ...


@overload
async def afirst(aiterable: AsyncIterable[T], /, *, default: D) -> T | D: ...


async def afirst(aiterable: AsyncIterable[Any], /, *, default: Any = ...) -> Any:
    """Return the first item of ``aiterable``.

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
        The first item.

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
    item = await anext(aiterator, default)

    if item is ...:
        detail = "afirst(): empty iterable"
        raise IndexError(detail) from None

    return item
