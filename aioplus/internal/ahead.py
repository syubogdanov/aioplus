from collections.abc import AsyncIterable
from typing import SupportsIndex, TypeVar

from aioplus.internal import cast
from aioplus.internal.aislice import aislice


T = TypeVar("T")


def ahead(aiterable: AsyncIterable[T], /, *, n: SupportsIndex) -> AsyncIterable[T]:
    """Return the first ``n`` items of the ``aiterable``.

    Parameters
    ----------
    aiterable : AsyncIterable[T]
        An asynchronous iterable to retrieve items from.

    n : SupportsIndex
        The number of items to retrieve from the start.

    Returns
    -------
    AsyncIterable[T]
        An asynchronous iterable yielding the first ``n`` items of the ``aiterable``.

    Examples
    --------
    >>> import asyncio
    >>>
    >>> from aioplus import ahead, arange
    >>>
    >>> async def main() -> None:
    >>>     '''Run the program.'''
    >>>     async for num in ahead(arange(23), n=4):
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

    n = cast.to_non_negative_int(n, variable_name="n")

    return aislice(aiterable, n)
