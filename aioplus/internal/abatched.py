from collections.abc import AsyncIterable, AsyncIterator
from dataclasses import dataclass
from typing import Self, TypeVar

from aioplus.internal.aislice import aislice


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
        The asynchronous iterable.

    n : int
        The batch size.

    strict : bool, default False
        If :obj:`True`, raises :exc:`ValueError` if the total number of objects is not divisible
        by ``n``. If :obj:`False`, the last batch may be shorter than ``n``.

    Returns
    -------
    AsyncIterator[tuple[T, ...]]
        The asynchronous iterator.

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


@dataclass(repr=False)
class AbatchedIterator(AsyncIterator[tuple[T, ...]]):
    """An asynchronous iterator."""

    aiterator: AsyncIterator[T]
    n: int
    strict: bool

    def __post_init__(self) -> None:
        """Initialize the object."""
        self._finished_flg: bool = False

    def __aiter__(self) -> Self:
        """Return an asynchronous iterator."""
        return self

    async def __anext__(self) -> tuple[T, ...]:
        """Return the next item."""
        if self._finished_flg:
            raise StopAsyncIteration

        try:
            batch = [item async for item in aislice(self.aiterator, self.n)]

        except BaseException:
            self._finished_flg = True
            raise

        if not batch:
            self._finished_flg = True
            raise StopAsyncIteration

        if self.strict and len(batch) < self.n:
            self._finished_flg = True
            detail = "abatched(): incomplete batch"
            raise ValueError(detail)

        return tuple(batch)
