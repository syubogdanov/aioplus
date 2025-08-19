from collections.abc import AsyncIterable
from typing import SupportsIndex, TypeVar

from aioplus.internal.core.aislice import aislice
from aioplus.internal.utils import cast


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
    aiterable = cast.to_async_iterable(aiterable, variable_name="aiterable")
    n = cast.to_non_negative_int(n, variable_name="n")

    return aislice(aiterable, n)
