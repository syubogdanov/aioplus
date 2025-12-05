from collections.abc import AsyncIterator, Iterable, Iterator
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from functools import partial
from typing import TypeVar

from aioplus.internal.awaitify import awaitify
from aioplus.internal.utils.abc import AioplusIterator


T = TypeVar("T")


def anextify(
    iterable: Iterable[T],
    /,
    *,
    executor: ThreadPoolExecutor | None = None,
) -> AsyncIterator[T]:
    """Make ``iterable`` asynchronous.

    Parameters
    ----------
    iterable : Iterable[T]
        Iterable.

    executor : ThreadPoolExecutor, optional
        Executor.

    Returns
    -------
    AsyncIterator[T]
        Iterator.

    Notes
    -----
    * If ``executor`` is :obj:`None`, then the default one is used (usually, a thread pool).

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

    iterator = iter(iterable)
    return AnextifyIterator(iterator, executor)


@dataclass(repr=False)
class AnextifyIterator(AioplusIterator[T]):
    """An asynchronous iterator."""

    iterator: Iterator[T]
    executor: ThreadPoolExecutor | None

    async def __aioplus__(self) -> T:
        """Return the next item."""
        func = partial(next, self.iterator, ...)
        afunc = awaitify(func, executor=self.executor)

        item = await afunc()
        if item is ...:
            raise StopAsyncIteration

        return item
