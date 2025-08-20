from collections.abc import AsyncIterable, Callable
from typing import Any, TypeAlias, TypeVar, overload

from aioplus.internal import coercions
from aioplus.internal.sentinels import Sentinel
from aioplus.internal.typing import SupportsDunderGT, SupportsDunderLT


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
    default: Any = Sentinel,
) -> tuple[Any, Any]:
    """Return the smallest and the largest item in ``aiterable``.

    Parameters
    ----------
    aiterable : AsyncIterable[T]
        An asynchronous iterable of objects.

    key : Callable[[T], SupportsRichComparison], optional
        A function that extracts a comparison key from each element in the iterable.

    default : tuple[D1, D2], optional
        The default values to return if the iterable is empty.

    Returns
    -------
    tuple[T | D1, T | D2]
        The smallest and the largest item in the iterable or the default values.

    Examples
    --------
    >>> import asyncio
    >>>
    >>> from aioplus import aminmax, arange
    >>>
    >>> async def main() -> None:
    >>>     '''Run the program.'''
    >>>     aiterable = arange(23)
    >>>     smallest, largest = await aminmax(aiterable)
    >>>     print(f'min(aiterable) == {smallest}')
    >>>     print(f'max(aiterable) == {largest}')
    >>>
    >>> if __name__ == '__main__':
    >>>     asyncio.run(main())

    See Also
    --------
    :func:`min`
    :func:`max`
    """
    aiterable = coercions.to_async_iterable(aiterable, variable_name="aiterable")

    if key is not None:
        key = coercions.to_callable(key, variable_name="key")

    if default is not Sentinel:
        default = coercions.to_pair(default, variable_name="default")

    aiterator = aiter(aiterable)

    try:
        smallest = largest = await anext(aiterator)

    except StopAsyncIteration:
        if default is not Sentinel:
            return default

        detail = "aminmax(): empty iterable"
        raise ValueError(detail) from None

    async for value in aiterator:
        smallest = min(smallest, value, key=key)
        largest = max(largest, value, key=key)

    return (smallest, largest)
