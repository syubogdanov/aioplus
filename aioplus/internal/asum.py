from collections.abc import AsyncIterable
from typing import Any, Literal, Protocol, TypeVar, overload

from aioplus.internal.typing import SupportsAdd, SupportsRAdd


AddableT1 = TypeVar("AddableT1", bound=SupportsAdd[Any, Any])
AddableT2 = TypeVar("AddableT2", bound=SupportsAdd[Any, Any])


class SupportsSumWithNoDefaultGiven(SupportsAdd[Any, Any], SupportsRAdd[int, Any], Protocol):
    """An ABC with two abstract methods `__add__` and `__radd__`."""


SupportsSumNoDefaultT = TypeVar("SupportsSumNoDefaultT", bound=SupportsSumWithNoDefaultGiven)


@overload
async def asum(aiterable: AsyncIterable[bool | int], /, *, start: int = 0) -> int: ...


@overload
async def asum(
    aiterable: AsyncIterable[SupportsSumNoDefaultT],
    /,
) -> SupportsSumNoDefaultT | Literal[0]: ...


@overload
async def asum(
    aiterable: AsyncIterable[AddableT1],
    /,
    *,
    start: AddableT2,
) -> AddableT1 | AddableT2: ...


async def asum(aiterable: AsyncIterable[Any], /, *, start: Any = 0) -> Any:
    """Sum ``start`` and items of ``aiterable`` from left to right and return the total.

    Parameters
    ----------
    aiterable : AsyncIterable[T]
        An asynchronous iterable.

    start : T
        The initial value to start the summation from.

    Returns
    -------
    T
        The total sum of the items in the asynchronous iterable.

    Examples
    --------
    >>> aiterable = arange(23)
    >>> await asum(aiterable)
    253

    See Also
    --------
    :func:`sum`
    """
    if not isinstance(aiterable, AsyncIterable):
        detail = "'aiterable' must be 'AsyncIterable'"
        raise TypeError(detail)

    total = start
    async for value in aiterable:
        total += value

    return total
