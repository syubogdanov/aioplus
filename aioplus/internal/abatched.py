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
    >> import asyncio
    >>
    >> from aioplus import abatched, arange
    >>
    >> async def main() -> None:
    >>     '''Run the program.'''
    >>     async for batch in abatched(arange(23), n=4):
    >>         print(batch)
    >>
    >> if __name__ == '__main__':
    >>     asyncio.run(main())

    Notes
    -----
    - The final batch may be shorter than ``n``, unless ``strict`` is set to :obj:`True`.

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

    if n < 1:
        detail = "'n' must be at least one"
        raise ValueError(detail)

    if not isinstance(strict, bool):
        detail = "'strict' must be 'bool'"
        raise TypeError(detail)

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

        if len(batch) < self.n and self.strict:
            self._finished_flg = True
            detail = "abatched(): incomplete batch"
            raise ValueError(detail)

        return tuple(batch)
