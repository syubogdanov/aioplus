import asyncio

from collections.abc import AsyncIterable, AsyncIterator
from dataclasses import dataclass
from typing import Self, SupportsIndex


def acount(
    start: SupportsIndex = 0,
    step: SupportsIndex = 1,
) -> AsyncIterable[int]:
    """Return evenly spaced values beginning with ``start``.

    Parameters
    ----------
    start : int, default 0
        The initial value. Must be an object supporting :meth:`object.__index__`.

    step : int, default 1
        The difference between consecutive values. Must be an object supporting
        :meth:`object.__index__`.

    Returns
    -------
    AsyncIterable of int
        An infinite asynchronous iterable yielding integers, starting from ``start``
        and incremented by ``step``.

    Examples
    --------
    >>> import asyncio
    >>>
    >>> from aioplus import acount
    >>>
    >>> async def main() -> None:
    >>>     '''Run the program.'''
    >>>     async for num in acount(start=23, step=4):
    >>>         print(num)
    >>>
    >>> if __name__ == '__main__':
    >>>     asyncio.run(main())

    Notes
    -----
    - Yields control to the event loop before producing each value via :func:`asyncio.sleep(0.0)`.

    See Also
    --------
    :func:`itertools.count`
    """
    if not isinstance(start, SupportsIndex):
        detail = "'start' must be 'SupportsIndex'"
        raise TypeError(detail)

    if not isinstance(step, SupportsIndex):
        detail = "'step' must be 'SupportsIndex'"
        raise TypeError(detail)

    start = start.__index__()
    step = step.__index__()

    return AcountIterable(start, step)


@dataclass
class AcountIterable(AsyncIterable[int]):
    """An asynchronous iterable."""

    start: int
    step: int

    def __aiter__(self) -> AsyncIterator[int]:
        """Return an asynchronous iterator."""
        return AcountIterator(self.start, self.step)


@dataclass
class AcountIterator(AsyncIterator[int]):
    """An asynchronous iterator."""

    start: int
    step: int

    def __post_init__(self) -> None:
        """Initialize the object."""
        self._next_value = self.start

    def __aiter__(self) -> Self:
        """Return an asynchronous iterator."""
        return self

    async def __anext__(self) -> int:
        """Return the next value."""
        value = self._next_value
        self._next_value += self.step

        # Move to the next coroutine!
        await asyncio.sleep(0.0)

        return value
