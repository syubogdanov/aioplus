from collections.abc import AsyncIterable, Callable
from typing import Any, TypeAlias, TypeVar, overload

from aioplus.internal.typing import SupportsDunderGT, SupportsDunderLT


T = TypeVar("T")
D = TypeVar("D")

SupportsRichComparison: TypeAlias = SupportsDunderLT[Any] | SupportsDunderGT[Any]
SupportsRichComparisonT = TypeVar("SupportsRichComparisonT", bound=SupportsRichComparison)


@overload
async def amax(
    iterable: AsyncIterable[SupportsRichComparisonT],
    /,
    *,
    key: None = None,
) -> SupportsRichComparisonT: ...


@overload
async def amax(
    iterable: AsyncIterable[T],
    /,
    *,
    key: Callable[[T], SupportsRichComparison],
) -> T: ...


@overload
async def amax(
    iterable: AsyncIterable[SupportsRichComparisonT],
    /,
    *,
    key: None = None,
    default: T,
) -> SupportsRichComparisonT | T: ...


@overload
async def amax(
    iterable: AsyncIterable[T],
    /,
    *,
    key: Callable[[T], SupportsRichComparison],
    default: D,
) -> T | D: ...


async def amax(
    aiterable: AsyncIterable[Any],
    /,
    *,
    key: Callable[[Any], Any] | None = None,
    default: Any = ...,
) -> Any:
    """Return the largest item in ``aiterable``.

    Parameters
    ----------
    aiterable : AsyncIterable[T]
        The asynchronous iterable.

    key : Callable[[T], SupportsRichComparison], optional
        A function that extracts a comparison key from each element in the iterable.

    default : D, unset
        A default value to return if the iterable is empty.

    Returns
    -------
    T | D
        The largest item.

    Examples
    --------
    >>> aiterable = arange(23)
    >>> await amax(aiterable)
    22

    See Also
    --------
    :func:`max`
    """
    if not isinstance(aiterable, AsyncIterable):
        detail = "'aiterable' must be 'AsyncIterable'"
        raise TypeError(detail)

    if key is not None and not callable(key):
        detail = "'key' must be 'Callable' or 'None'"
        raise TypeError(detail)

    aiterator = aiter(aiterable)
    largest = await anext(aiterator, ...)

    if largest is not ...:
        async for item in aiterator:
            largest = max(largest, item, key=key)
        return largest

    if default is not ...:
        return default

    detail = "amax(): empty iterable"
    raise ValueError(detail) from None
