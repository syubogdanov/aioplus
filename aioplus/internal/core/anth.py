from collections.abc import AsyncIterable
from typing import Any, SupportsIndex, TypeVar, overload

from aioplus.internal.core.aenumerate import aenumerate
from aioplus.internal.utils import cast
from aioplus.internal.utils.enums import AioPlus


T1 = TypeVar("T1")
T2 = TypeVar("T2")


@overload
async def anth(aiterable: AsyncIterable[T1], /, *, n: SupportsIndex) -> T1: ...


@overload
async def anth(aiterable: AsyncIterable[T1], /, *, n: SupportsIndex, default: T2) -> T1 | T2: ...


async def anth(
    aiterable: AsyncIterable[Any],
    /,
    *,
    n: SupportsIndex,
    default: Any = AioPlus.SENTINEL,
) -> Any:
    """Return the nth item or a default value.

    Parameters
    ----------
    aiterable : AsyncIterable[T1]
        An asynchronous iterable to retrieve the nth item from.

    n : SupportsIndex
        The index of the item to retrieve, starting from 0.

    default : T2, optional
        A default value to return if the nth item does not exist.
        If not provided, :obj:`IndexError` will be raised if the nth item is not found.

    Returns
    -------
    T1 or T2
        The nth item or the default value.

    Examples
    --------
    >>> import asyncio
    >>>
    >>> from aioplus import anth, arange
    >>>
    >>> async def main() -> None:
    >>>     '''Run the program.'''
    >>>     aiterable = arange(23)
    >>>     value = await anth(aiterable, n=4)
    >>>     print(f'value = {value}')
    >>>
    >>> if __name__ == '__main__':
    >>>     asyncio.run(main())
    """
    aiterable = cast.to_async_iterable(aiterable, variable_name="aiterable")
    n = cast.to_non_negative_int(n, variable_name="n")

    async for index, value in aenumerate(aiterable):
        if index == n:
            return value

    if not isinstance(default, AioPlus):
        return default

    detail = "The iterable contains fewer than 'n' items"
    raise IndexError(detail)
