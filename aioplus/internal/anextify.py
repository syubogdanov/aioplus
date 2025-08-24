from collections.abc import AsyncIterable, AsyncIterator, Iterable, Iterator
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from typing import Self, TypeVar

from aioplus.internal.awaitify import awaitify
from aioplus.internal.sentinels import Sentinel


T = TypeVar("T")


def anextify(
    iterable: Iterable[T],
    /,
    *,
    executor: ThreadPoolExecutor | None = None,
) -> AsyncIterable[T]:
    """Make an iterable asynchronous.

    Parameters
    ----------
    iterable : Iterable[T]
        An iterable to be wrapped for asynchronous execution.

    executor : ThreadPoolExecutor, optional
        An optional :class:`concurrent.futures.ThreadPoolExecutor` to run the function in. If
        :obj:`None`, the default executor is used.

    Returns
    -------
    AsyncIterable[T]
        An asynchronous iterable that, when awaited, calls :meth:`object.__next__` in the executor.

    Examples
    --------
    >>> iterable = [0, 1, 2, 3, 4, 5]
    >>> aiterable = anextify(iterable)
    >>> [num async for num in aiterable]
    [0, 1, 2, 3, 4, 5]

    See Also
    --------
    :meth:`asyncio.loop.run_in_executor`
    """
    if not isinstance(iterable, Iterable):
        detail = "'iterable' must be 'Iterable'"
        raise TypeError(detail)

    if executor is not None and not isinstance(executor, ThreadPoolExecutor):
        detail = "'executor' must be 'ThreadPoolExecutor' or 'None'"
        raise TypeError(detail)

    return AnextifyIterable(iterable, executor)


@dataclass
class AnextifyIterable(AsyncIterable[T]):
    """An asynchronous iterable."""

    iterable: Iterable[T]
    executor: ThreadPoolExecutor | None

    def __aiter__(self) -> AsyncIterator[T]:
        """Return an asynchronous iterator."""
        iterator = iter(self.iterable)
        return AnextifyIterator(iterator, self.executor)


@dataclass
class AnextifyIterator(AsyncIterator[T]):
    """An asynchronous iterator."""

    iterator: Iterator[T]
    executor: ThreadPoolExecutor | None

    def __post_init__(self) -> None:
        """Initialize the object."""
        self._finished_flg: bool = False

    def __aiter__(self) -> Self:
        """Return an asynchronous iterator."""
        return self

    async def __anext__(self) -> T:
        """Return the next value."""
        if self._finished_flg:
            raise StopAsyncIteration

        # Use `next`, not `__next__`. See the comment below
        awaitified = awaitify(next, executor=self.executor)

        try:
            # Use the default value because `StopIteration` cannot be raised into a `Future`!
            value = await awaitified(self.iterator, Sentinel.EMPTY)  # type: ignore[call-arg]

        except Exception:
            self._finished_flg = True
            raise

        if value is Sentinel.EMPTY:
            self._finished_flg = True
            raise StopAsyncIteration

        return value
