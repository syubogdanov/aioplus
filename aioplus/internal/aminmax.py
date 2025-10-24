from collections.abc import AsyncIterable, Callable
from typing import Any, TypeAlias, TypeVar, overload

from aioplus.internal.utils.typing import SupportsDunderGT, SupportsDunderLT


T = TypeVar("T")

D1 = TypeVar("D1")
D2 = TypeVar("D2")

SupportsRichComparison: TypeAlias = SupportsDunderLT[Any] | SupportsDunderGT[Any]
SupportsRichComparisonT = TypeVar("SupportsRichComparisonT", bound=SupportsRichComparison)


@overload
async def aminmax(
    iterable: AsyncIterable[SupportsRichComparisonT],
    /,
    *,
    key: None = None,
) -> tuple[SupportsRichComparisonT, SupportsRichComparisonT]: ...


@overload
async def aminmax(
    iterable: AsyncIterable[T],
    /,
    *,
    key: Callable[[T], SupportsRichComparison],
) -> tuple[T, T]: ...


@overload
async def aminmax(
    iterable: AsyncIterable[SupportsRichComparisonT],
    /,
    *,
    key: None = None,
    default: tuple[T, T],
) -> tuple[SupportsRichComparisonT | T, SupportsRichComparisonT | T]: ...


@overload
async def aminmax(
    iterable: AsyncIterable[T],
    /,
    *,
    key: Callable[[T], SupportsRichComparison],
    default: tuple[D1, D2],
) -> tuple[T | D1, T | D2]: ...


async def aminmax(
    aiterable: AsyncIterable[Any],
    /,
    *,
    key: Callable[[Any], Any] | None = None,
    default: Any = ...,
) -> tuple[Any, Any]:
    """Return the smallest and the largest items in ``aiterable``.

    Parameters
    ----------
    aiterable : AsyncIterable[T]
        The asynchronous iterable.

    key : Callable[[T], SupportsRichComparison], optional
        A function that extracts a comparison key from each element in the iterable.

    default : tuple[D1, D2], unset
        Default values to return if the iterable is empty.

    Returns
    -------
    tuple[T | D1, T | D2]
        The smallest and the largest items.

    Examples
    --------
    >>> aiterable = arange(23)
    >>> await aminmax(aiterable)
    (0, 22)

    Notes
    -----
    * This function is not comparison-optimized.

    See Also
    --------
    :func:`min`
    :func:`max`
    """
    if not isinstance(aiterable, AsyncIterable):
        detail = "'aiterable' must be 'AsyncIterable'"
        raise TypeError(detail)

    if key is not None and not callable(key):
        detail = "'key' must be 'Callable' or 'None'"
        raise TypeError(detail)

    if default is not ... and not isinstance(default, tuple):
        detail = "'default' must be 'tuple[D1, D2]'"
        raise TypeError(detail)

    if default is not ... and len(default) != 2:
        detail = "'len(default)' must be '2'"
        raise ValueError(detail)

    aiterator = aiter(aiterable)
    smallest = largest = await anext(aiterator, ...)

    if smallest is not ...:
        async for item in aiterator:
            smallest = min(smallest, item, key=key)
            largest = max(largest, item, key=key)
        return (smallest, largest)

    if default is ...:
        detail = "aminmax(): empty iterable"
        raise ValueError(detail) from None

    return default
