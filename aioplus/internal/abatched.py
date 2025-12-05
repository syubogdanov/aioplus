from collections.abc import AsyncIterable, AsyncIterator
from dataclasses import dataclass
from typing import TypeVar

from aioplus.internal.aislice import aislice
from aioplus.internal.utils.abc import AioplusIterator


T = TypeVar("T")


def abatched(
    aiterable: AsyncIterable[T],
    /,
    *,
    n: int,
    strict: bool = False,
) -> AsyncIterator[tuple[T, ...]]:
    """Iterate ``aiterable`` by batches of length ``n``.

    Parameters
    ----------
    aiterable : AsyncIterable[T]
        Iterable.

    n : int
        Batch size.

    strict : bool, default False
        Strictness.

    Returns
    -------
    AsyncIterator[tuple[T, ...]]
        Iterator.

    Notes
    -----
    * If ``strict`` is :obj:`True` and the total number of objects is not divisible by ``n``, then
      raises :exc:`ValueError`. If :obj:`False`, the last batch may be shorter than ``n``.

    Examples
    --------
    >>> aiterable = arange(23)
    >>> [batch async for batch in abatched(aiterable, n=3)]
    [(0, 1, 2), (3, 4, 5), ..., (18, 19, 20), (21, 22)]

    See Also
    --------
    :func:`itertools.batched`
    """
    if not isinstance(aiterable, AsyncIterable):
        detail = "'aiterable' must be 'AsyncIterable'"
        raise TypeError(detail)

    if not isinstance(n, int):
        detail = "'n' must be 'int'"
        raise TypeError(detail)

    if n <= 0:
        detail = "'n' must be positive"
        raise ValueError(detail)

    if not isinstance(strict, bool):
        detail = "'strict' must be 'bool'"
        raise TypeError(detail)

    aiterator = aiter(aiterable)
    return AbatchedIterator(aiterator, n, strict)


@dataclass
class AbatchedIterator(AioplusIterator[tuple[T, ...]]):
    """An asynchronous iterator."""

    aiterator: AsyncIterator[T]
    n: int
    strict: bool

    async def __aioplus__(self) -> tuple[T, ...]:
        """Return the next item."""
        batch = [item async for item in aislice(self.aiterator, self.n)]

        if not batch:
            raise StopAsyncIteration

        if self.strict and len(batch) < self.n:
            detail = "abatched(): incomplete batch"
            raise ValueError(detail)

        return tuple(batch)
