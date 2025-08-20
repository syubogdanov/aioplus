from collections.abc import AsyncIterable, Callable
from typing import Any, TypeAlias, TypeVar, overload

from aioplus.internal import coercions
from aioplus.internal.sentinels import Sentinel
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
    default: Any = Sentinel,
) -> Any:
    """Return the largest item in ``aiterable``.

    Parameters
    ----------
    aiterable : AsyncIterable[T]
        An asynchronous iterable of objects.

    key : Callable[[T], SupportsRichComparison], optional
        A function that extracts a comparison key from each element in the iterable.

    default : D, optional
        A default value to return if the iterable is empty.

    Returns
    -------
    T or D
        The largest item in the iterable or the default value.

    Examples
    --------
    >>> import asyncio
    >>>
    >>> from aioplus import amax, arange
    >>>
    >>> async def main() -> None:
    >>>     '''Run the program.'''
    >>>     aiterable = arange(23)
    >>>     largest = await amax(aiterable)
    >>>     print(f'max(aiterable) == {largest}')
    >>>
    >>> if __name__ == '__main__':
    >>>     asyncio.run(main())

    See Also
    --------
    :func:`max`
    """
    aiterable = coercions.to_async_iterable(aiterable, variable_name="aiterable")

    if key is not None:
        key = coercions.to_callable(key, variable_name="key")

    aiterator = aiter(aiterable)

    try:
        largest = await anext(aiterator)

    except StopAsyncIteration:
        if default is not Sentinel:
            return default

        detail = "amax(): empty iterable"
        raise ValueError(detail) from None

    async for value in aiterator:
        largest = max(largest, value, key=key)

    return largest
