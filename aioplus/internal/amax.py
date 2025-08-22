from collections.abc import AsyncIterable, Callable
from typing import Any, TypeAlias, TypeVar, overload

from aioplus.internal import coercions
from aioplus.internal.aminmax import aminmax
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
    default: Any = Sentinel.UNSET,
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
    >>> aiterable = arange(23)
    >>> await amax(aiterable)
    22

    See Also
    --------
    :func:`max`
    """
    aiterable = coercions.be_async_iterable(aiterable, variable_name="aiterable")

    if key is not None:
        key = coercions.be_callable(key, variable_name="key")

    _, largest = await aminmax(aiterable, key=key, default=(Sentinel.EMPTY, Sentinel.EMPTY))
    if largest is not Sentinel.EMPTY:
        return largest

    if default is not Sentinel.UNSET:
        return default

    detail = "amax(): empty iterable"
    raise ValueError(detail) from None
