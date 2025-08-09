from collections.abc import AsyncIterable, AsyncIterator
from dataclasses import dataclass
from typing import Self, SupportsIndex, TypeVar, overload


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


def aislice(  # noqa: C901, PLR0912
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
    >>> import asyncio
    >>>
    >>> from aioplus import aislice, arange
    >>>
    >>> async def main() -> None:
    >>>     '''Run the program.'''
    >>>     async for num in aislice(arange(23), 4):
    >>>         print(num)
    >>>
    >>> if __name__ == '__main__':
    >>>     asyncio.run(main())

    See Also
    --------
    :func:`itertools.islice`
    """
    if not isinstance(aiterable, AsyncIterable):
        detail = "'aiterable' must be 'AsyncIterable'"
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

    if not isinstance(start, SupportsIndex):
        detail = "'start' must be 'SupportsIndex'"
        raise TypeError(detail)

    if not isinstance(step, SupportsIndex):
        detail = "'step' must be 'SupportsIndex'"
        raise TypeError(detail)

    if not isinstance(stop, SupportsIndex):
        detail = "'stop' must be 'SupportsIndex'"
        raise TypeError(detail)

    start = start.__index__()
    stop = stop.__index__()
    step = step.__index__()

    if not isinstance(start, int):
        detail = "'start.__index__()' must be 'int'"
        raise TypeError(detail)

    if not isinstance(stop, int):
        detail = "'stop.__index__()' must be 'int'"
        raise TypeError(detail)

    if not isinstance(step, int):
        detail = "'step.__index__()' must be 'int'"
        raise TypeError(detail)

    if start < 0:
        detail = "'start' must be non-negative"
        raise ValueError(detail)

    if stop < 0:
        detail = "'stop' must be non-negative"
        raise ValueError(detail)

    if step <= 0:
        detail = "'step' must be positive"
        raise ValueError(detail)

    return IsliceIterable(aiterable, start, stop, step)


@dataclass
class IsliceIterable(AsyncIterable[T]):
    """An asynchronous slice iterable."""

    aiterable: AsyncIterable[T]
    start: int
    stop: int
    step: int

    def __aiter__(self) -> AsyncIterator[T]:
        """Return an asynchronous iterator."""
        aiterator = aiter(self.aiterable)
        return IsliceIterator(aiterator, self.start, self.stop, self.step)


@dataclass
class IsliceIterator(AsyncIterator[T]):
    """An asynchronous slice iterator."""

    aiterator: AsyncIterator[T]
    start: int
    stop: int
    step: int

    def __post_init__(self) -> None:
        """Initialize the object."""
        self._finished_flg: bool = False
        self._next: int = 0
        self._yield: int = self.start

    def __aiter__(self) -> Self:
        """Return an asynchronous iterator."""
        return self

    async def __anext__(self) -> T:
        """Return the next value."""
        if self._finished_flg:
            raise StopAsyncIteration

        if self._yield >= self.stop:
            self._finished_flg = True
            raise StopAsyncIteration

        for _ in range(self._yield - self._next):
            try:
                await anext(self.aiterator)
                self._next += 1

            except Exception:
                self._finished_flg = True
                raise

        try:
            value = await anext(self.aiterator)
            self._next += 1

        except Exception:
            self._finished_flg = True
            raise

        self._yield += self.step

        return value
