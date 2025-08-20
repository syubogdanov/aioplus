from collections.abc import AsyncIterable, AsyncIterator
from dataclasses import dataclass
from typing import Self, SupportsIndex, TypeVar, overload

from aioplus.internal.coercions import to_async_iterable, to_non_negative_int, to_positive_int


T = TypeVar("T")


@overload
def aislice(aiterable: AsyncIterable[T], stop: SupportsIndex, /) -> AsyncIterable[T]: ...


@overload
def aislice(
    aiterable: AsyncIterable[T],
    start: SupportsIndex,
    stop: SupportsIndex,
    /,
) -> AsyncIterable[T]: ...


@overload
def aislice(
    aiterable: AsyncIterable[T],
    start: SupportsIndex,
    stop: SupportsIndex,
    step: SupportsIndex,
    /,
) -> AsyncIterable[T]: ...


def aislice(
    aiterable: AsyncIterable[T],
    start: SupportsIndex,
    stop: SupportsIndex | None = None,
    step: SupportsIndex | None = None,
    /,
) -> AsyncIterable[T]:
    """Return selected elements from the iterable.

    Parameters
    ----------
    aiterable : AsyncIterable of T
        An asynchronous iterable of objects to slice.

    start : int
        The index of the first object to include. If ``stop`` is :obj:`None`, treated as the end
        index, and slicing starts from ``0``.

    stop : int, optional
        The index at which to stop (exclusive). If not provided, ``start`` is interpreted
        as ``stop``, and slicing starts from ``0``.

    step : int, optional
        The difference between consecutive values. Defaults to ``1``.

    Returns
    -------
    AsyncIterable of T
        An asynchronous iterable yielding selected objects according to the slice parameters.

    Examples
    --------
    >>> aiterable = arange(2003)
    >>> [num async for num in aislice(aiterable, 4, 23)]
    [4, 5, 6, 7, 8, ..., 20, 21, 22]

    See Also
    --------
    :func:`itertools.islice`
    """
    if stop is None and step is not None:
        detail = "'step' is not specified but 'stop' is"
        raise ValueError(detail)

    if stop is None:
        stop = start
        start = 0
        step = 1

    if step is None:
        step = 1

    aiterable = to_async_iterable(aiterable, variable_name="aiterable")
    start = to_non_negative_int(start, variable_name="start")
    stop = to_non_negative_int(stop, variable_name="stop")
    step = to_positive_int(step, variable_name="step")

    return AisliceIterable(aiterable, start, stop, step)


@dataclass
class AisliceIterable(AsyncIterable[T]):
    """An asynchronous slice iterable."""

    aiterable: AsyncIterable[T]
    start: int
    stop: int
    step: int

    def __aiter__(self) -> AsyncIterator[T]:
        """Return an asynchronous iterator."""
        aiterator = aiter(self.aiterable)
        return AisliceIterator(aiterator, self.start, self.stop, self.step)


@dataclass
class AisliceIterator(AsyncIterator[T]):
    """An asynchronous slice iterator."""

    aiterator: AsyncIterator[T]
    start: int
    stop: int
    step: int

    def __post_init__(self) -> None:
        """Initialize the object."""
        self._next_index: int = 0
        self._yield_index: int = self.start
        self._finished_flg: bool = False

    def __aiter__(self) -> Self:
        """Return an asynchronous iterator."""
        return self

    async def __anext__(self) -> T:
        """Return the next value."""
        if self._finished_flg:
            raise StopAsyncIteration

        if self._yield_index >= self.stop:
            self._finished_flg = True
            raise StopAsyncIteration

        # Skip values until reaching the yield index
        count = self._yield_index - self._next_index

        try:
            for _ in range(count + 1):
                value = await anext(self.aiterator)
                self._next_index += 1

        except StopAsyncIteration:
            self._finished_flg = True
            raise

        self._yield_index += self.step

        return value
