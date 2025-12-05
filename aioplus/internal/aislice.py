from collections.abc import AsyncIterable, AsyncIterator
from dataclasses import dataclass
from types import EllipsisType
from typing import TypeVar, overload

from aioplus.internal.utils.abc import AioplusIterator


T = TypeVar("T")


@overload
def aislice(aiterable: AsyncIterable[T], stop: int, /) -> AsyncIterator[T]: ...


@overload
def aislice(aiterable: AsyncIterable[T], start: int, stop: int, /) -> AsyncIterator[T]: ...


@overload
def aislice(
    aiterable: AsyncIterable[T],
    start: int,
    stop: int,
    step: int,
    /,
) -> AsyncIterator[T]: ...


def aislice(
    aiterable: AsyncIterable[T],
    start: int,
    stop: int | EllipsisType = ...,
    step: int | EllipsisType = ...,
    /,
) -> AsyncIterator[T]:
    """Return selected items from ``aiterable``.

    Parameters
    ----------
    aiterable : AsyncIterable[T]
        Iterable.

    start : int
        Start.

    stop : int, unset
        Stop.

    step : int, unset
        Step.

    Returns
    -------
    AsyncIterator[T]
        Iterator.

    Examples
    --------
    >>> aiterable = arange(2003)
    >>> [num async for num in aislice(aiterable, 4, 23)]
    [4, 5, 6, 7, 8, ..., 20, 21, 22]

    See Also
    --------
    :func:`itertools.islice`
    """
    if not isinstance(aiterable, AsyncIterable):
        detail = "'aiterable' must be 'AsyncIterable'"
        raise TypeError(detail)

    if not isinstance(start, int):
        detail = "'start' must be 'int'"
        raise TypeError(detail)

    if (stop is not ...) and not isinstance(stop, int):
        detail = "'stop' must be 'int'"
        raise TypeError(detail)

    if (step is not ...) and not isinstance(step, int):
        detail = "'step' must be 'int'"
        raise TypeError(detail)

    if (stop is ...) and (step is not ...):
        detail = "'step' must be 'int'"
        raise TypeError(detail)

    if stop is ...:
        stop = start
        start = 0
        step = 1

    if step is ...:
        step = 1

    if start < 0:
        detail = "'start' must be non-negative"
        raise ValueError(detail)

    if stop < 0:
        detail = "'stop' must be non-negative"
        raise ValueError(detail)

    if step <= 0:
        detail = "'step' must be positive"
        raise ValueError(detail)

    aiterator = aiter(aiterable)
    return AisliceIterator(aiterator, start, stop, step)


@dataclass(repr=False)
class AisliceIterator(AioplusIterator[T]):
    """An asynchronous iterator."""

    aiterator: AsyncIterator[T]
    start: int
    stop: int
    step: int

    def __post_init__(self) -> None:
        """Initialize the object."""
        self._next = 0
        self._yield_at = self.start

    async def __aioplus__(self) -> T:
        """Return the next item."""
        if self._yield_at >= self.stop:
            raise StopAsyncIteration

        for _ in range(self._yield_at - self._next):
            await anext(self.aiterator)
            self._next += 1

        item = await anext(self.aiterator)

        self._next += 1
        self._yield_at += self.step

        return item
