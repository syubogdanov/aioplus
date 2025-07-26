import asyncio

from collections.abc import AsyncIterable, AsyncIterator
from dataclasses import dataclass
from typing import Self, SupportsIndex, overload


@overload
def arange(stop: SupportsIndex, /) -> AsyncIterable[int]: ...


@overload
def arange(start: SupportsIndex, stop: SupportsIndex, /) -> AsyncIterable[int]: ...


@overload
def arange(
    start: SupportsIndex,
    stop: SupportsIndex,
    step: SupportsIndex,
    /,
) -> AsyncIterable[int]: ...


def arange(
    start: SupportsIndex,
    stop: SupportsIndex | None = None,
    step: SupportsIndex | None = None,
    /,
) -> AsyncIterable[int]:
    """Iterate over a range of integers.

    Parameters
    ----------
    start : int
        The starting value of the sequence (inclusive). If ``stop`` is :obj:`None`, this argument
        is treated as the end value, and the sequence starts from ``0``.

    stop : int, optional
        The end value of the sequence (exclusive). If not provided, ``start`` is interpreted
        as the end and the sequence begins from ``0``.

    step : int, optional
        The difference between consecutive values. Defaults to ``1`` if not specified. May be
        negative to produce a decreasing sequence.

    Returns
    -------
    AsyncIterable of int
        An asynchronous iterable yielding values from ``start`` to ``stop``, separated by ``step``.

    Examples
    --------
    >>> import asyncio
    >>>
    >>> from aioplus import arange
    >>>
    >>> async def main() -> None:
    >>>     '''Run the program.'''
    >>>     async for num in arange(2304):
    >>>         print(num)
    >>>
    >>> if __name__ == '__main__':
    >>>     asyncio.run(main())

    See Also
    --------
    :func:`range`
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

    if not isinstance(start, SupportsIndex):
        detail = "'start' must be 'SupportsIndex'"
        raise TypeError(detail)

    if not isinstance(stop, SupportsIndex):
        detail = "'stop' must be 'SupportsIndex'"
        raise TypeError(detail)

    if not isinstance(step, SupportsIndex):
        detail = "'step' must be 'SupportsIndex'"
        raise TypeError(detail)

    start = start.__index__()
    stop = stop.__index__()
    step = step.__index__()

    if step == 0:
        detail = "'step' must not be zero"
        raise ValueError(detail)

    return ArangeIterable(start, stop, step)


@dataclass
class ArangeIterable(AsyncIterable[int]):
    """An asynchronous range iterable."""

    start: int
    stop: int
    step: int

    def __aiter__(self) -> AsyncIterator[int]:
        """Return an asynchronous iterator."""
        return ArangeIterator(self.start, self.stop, self.step)


@dataclass
class ArangeIterator(AsyncIterator[int]):
    """An asynchronous range iterator."""

    start: int
    stop: int
    step: int

    def __post_init__(self) -> None:
        """Initialize the object."""
        self._next_value = self.start

    def __aiter__(self) -> Self:
        """Return an asynchronous iterator."""
        return self

    async def __anext__(self) -> int:
        """Return the next value."""
        if self.step > 0 and self._next_value >= self.stop:
            raise StopAsyncIteration

        if self.step < 0 and self._next_value <= self.stop:
            raise StopAsyncIteration

        value = self._next_value
        self._next_value += self.step

        # Move to the next coroutine!
        await asyncio.sleep(0.0)

        return value
