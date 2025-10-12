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
) -> AsyncIterable[tuple[T, ...]]:
    """Iterate over ``aiterable`` by batches of length ``n``.

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
    AsyncIterable[tuple[T, ...]]
        The asynchronous iterable.

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

    return AbatchedIterable(aiterable, n, strict)


@dataclass(repr=False)
class AbatchedIterable(AsyncIterable[tuple[T, ...]]):
    """An asynchronous iterable."""

    aiterable: AsyncIterable[T]
    n: int
    strict: bool

    def __aiter__(self) -> AsyncIterator[tuple[T, ...]]:
        """Return an asynchronous iterator."""
        aiterator = aiter(self.aiterable)
        return AbatchedIterator(aiterator, self.n, self.strict)


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
        """Return the next value."""
        if self._finished_flg:
            raise StopAsyncIteration

        try:
            batch = [value async for value in aislice(self.aiterator, self.n)]

        except Exception:
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
