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
        Iterable.

    default : D, unset
        Default.

    Returns
    -------
    T | D
        Item.

    Notes
    -----
    * If ``aiterable`` is empty and ``default`` is unset, then :obj:`IndexError` is raised.

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
