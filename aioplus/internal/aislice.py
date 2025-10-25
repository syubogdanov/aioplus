from collections.abc import AsyncIterable, AsyncIterator
from dataclasses import dataclass
from typing import Self, TypeVar, overload


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
    stop: int | None = None,
    step: int | None = None,
    /,
) -> AsyncIterator[T]:
    """Return selected items from ``aiterable``.

    Parameters
    ----------
    aiterable : AsyncIterable[T]
        The asynchronous iterable.

    start : int
        The index of the first item to include. If ``stop`` is :obj:`None`, treated as the end
        index, and slicing starts from ``0``.

    stop : int, optional
        The index at which to stop (exclusive). If not provided, ``start`` is interpreted
        as ``stop``, and slicing starts from ``0``.

    step : int, optional
        The step between consecutives. Defaults to ``1``.

    Returns
    -------
    AsyncIterator[T]
        The asynchronous iterator.

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

    if stop is not None and not isinstance(stop, int):
        detail = "'stop' must be 'int'"
        raise TypeError(detail)

    if step is not None and not isinstance(step, int):
        detail = "'step' must be 'int'"
        raise TypeError(detail)

    if stop is None and step is not None:
        detail = "'step' is not specified but 'stop' is"
        raise ValueError(detail)

    if stop is None:
        stop = start
        start = 0
        step = 1

    if step is None:
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
        """Return the next item."""
        if self._finished_flg:
            raise StopAsyncIteration

        if self._yield_index >= self.stop:
            self._finished_flg = True
            raise StopAsyncIteration

        # Skip items until reaching the yield index
        count = self._yield_index - self._next_index

        try:
            for _ in range(count + 1):
                item = await anext(self.aiterator)
                self._next_index += 1

        except (StopAsyncIteration, BaseException):
            self._finished_flg = True
            raise

        self._yield_index += self.step

        return item
