from collections.abc import AsyncIterable
from typing import Any, TypeVar, overload

from aioplus.internal.coercions import to_async_iterable
from aioplus.internal.sentinels import Sentinel


T = TypeVar("T")
D = TypeVar("D")


@overload
async def afirst(aiterable: AsyncIterable[T], /) -> T: ...


@overload
async def afirst(aiterable: AsyncIterable[T], /, *, default: D) -> T | D: ...


async def afirst(aiterable: AsyncIterable[Any], /, *, default: Any = Sentinel) -> Any:
    """Return the first item of the ``aiterable``.

    Parameters
    ----------
    aiterable : AsyncIterable[T]
        An asynchronous iterable to retrieve the item from.

    default : D, optional
        A default value to return if the iterable is empty.
        If not provided, :obj:`IndexError` will be raised if the iterable is empty.

    Returns
    -------
    T or D
        The first item of ``aiterable`` or the default value.

    Examples
    --------
    >>> import asyncio
    >>>
    >>> from aioplus import afirst, arange
    >>>
    >>> async def main() -> None:
    >>>     '''Run the program.'''
    >>>     aiterable = arange(4, 23)
    >>>     num = await afirst(aiterable)
    >>>     print(f'aiterable[0] = {num}')
    >>>
    >>> if __name__ == '__main__':
    >>>     asyncio.run(main())
    """
    aiterable = to_async_iterable(aiterable, variable_name="aiterable")

    aiterator = aiter(aiterable)
    value = await anext(aiterator, default)

    if value is not Sentinel:
        return value

    detail = "afirst(): empty iterable"
    raise IndexError(detail) from None
