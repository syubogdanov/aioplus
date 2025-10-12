from collections.abc import AsyncIterable, AsyncIterator, Iterable, Iterator
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from functools import partial
from typing import Self, TypeVar

from aioplus.internal.awaitify import awaitify


T = TypeVar("T")


def anextify(
    iterable: Iterable[T],
    /,
    *,
    executor: ThreadPoolExecutor | None = None,
) -> AsyncIterable[T]:
    """Make ``iterable`` asynchronous.

    Parameters
    ----------
    iterable : Iterable[T]
        The synchronous iterable.

    executor : ThreadPoolExecutor, optional
        An optional :class:`concurrent.futures.ThreadPoolExecutor` to run the iterable in. If
        :obj:`None`, the default executor is used.

    Returns
    -------
    AsyncIterable[T]
        The asynchronous iterable.

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


@dataclass(repr=False)
class AnextifyIterable(AsyncIterable[T]):
    """An asynchronous iterable."""

    iterable: Iterable[T]
    executor: ThreadPoolExecutor | None

    def __aiter__(self) -> AsyncIterator[T]:
        """Return an asynchronous iterator."""
        iterator = iter(self.iterable)
        return AnextifyIterator(iterator, self.executor)


@dataclass(repr=False)
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
        """Return the next item."""
        if self._finished_flg:
            raise StopAsyncIteration

        func = partial(next, self.iterator, ...)
        afunc = awaitify(func, executor=self.executor)

        try:
            item = await afunc()

        except Exception:
            self._finished_flg = True
            raise

        if item is ...:
            self._finished_flg = True
            raise StopAsyncIteration

        return item
