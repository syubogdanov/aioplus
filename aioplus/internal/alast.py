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
