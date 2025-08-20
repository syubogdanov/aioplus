from collections.abc import AsyncIterable, AsyncIterator
from dataclasses import dataclass
from typing import Self, TypeVar

from aioplus.internal.aislice import aislice
from aioplus.internal.coercions import to_async_iterable, to_bool, to_positive_int


T = TypeVar("T")


def abatched(
    aiterable: AsyncIterable[T],
    /,
    *,
    n: int,
    strict: bool = False,
) -> AsyncIterable[tuple[T, ...]]:
    """Batch data from the `aiterable` into tuples of length ``n``.

    Parameters
    ----------
    aiterable : AsyncIterable of T
        An asynchronous iterable of elements to be grouped into batches.

    n : int
        The batch size. Each tuple will contain up to ``n`` elements.

    strict : bool, default False
        If :obj:`True`, raises a :exc:`ValueError` if the total number of objects is not divisible
        by ``n``. If :obj:`False`, the last batch may be shorter than ``n``.

    Returns
    -------
    AsyncIterable of tuple[T, ...]
        An asynchronous iterable yielding tuples of at most ``n`` elements.

    Examples
    --------
    >>> aiterable = arange(23)
    >>> [batch async for batch in abatched(aiterable, n=3)]
    [(0, 1, 2), (3, 4, 5), ..., (18, 19, 20), (21, 22)]

    Notes
    -----
    - The final batch may be shorter than ``n``, unless ``strict`` is set to :obj:`True`.

    See Also
    --------
    :func:`itertools.batched`
    """
    aiterable = to_async_iterable(aiterable, variable_name="aiterable")
    n = to_positive_int(n, variable_name="n")
    strict = to_bool(strict, variable_name="strict")

    return AbatchedIterable(aiterable, n, strict)


@dataclass
class AbatchedIterable(AsyncIterable[tuple[T, ...]]):
    """An asynchronous iterable that batches data."""

    aiterable: AsyncIterable[T]
    n: int
    strict: bool

    def __aiter__(self) -> AsyncIterator[tuple[T, ...]]:
        """Return an asynchronous iterator."""
        aiterator = aiter(self.aiterable)
        return AbatchedIterator(aiterator, self.n, self.strict)


@dataclass
class AbatchedIterator(AsyncIterator[tuple[T, ...]]):
    """An asynchronous iterator that batches data."""

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
