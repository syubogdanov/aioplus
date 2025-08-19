from collections.abc import AsyncIterable

from aioplus.internal.utils import cast
from aioplus.internal.utils.typing import SupportsBool


async def aany(aiterable: AsyncIterable[SupportsBool], /) -> bool:
    """
    Return :obj:`True` if any element of the async iterable evaluates to :obj:`True`.

    Parameters
    ----------
    aiterable : AsyncIterable of SupportsBool
        An asynchronous iterable of objects supporting :meth:`object.__bool__`.

    Returns
    -------
    :class:`bool`
        :obj:`True` if any element evaluates to :obj:`True`.
        :obj:`False` if all elements evaluate to :obj:`False`, or if the iterable is empty.

    Examples
    --------
    >>> import asyncio
    >>>
    >>> from aioplus import aany, arange
    >>>
    >>> async def main() -> None:
    >>>     '''Run the program.'''
    >>>     aiterable = (num % 2 == 0 async for num in arange(2304))
    >>>     flg = await aany(aiterable)
    >>>
    >>> if __name__ == '__main__':
    >>>     asyncio.run(main())

    Notes
    -----
    - Short-circuits on the first object that evaluates to :obj:`True`.

    See Also
    --------
    :func:`any`
    """
    aiterable = cast.to_async_iterable(aiterable, variable_name="aiterable")

    async for value in aiterable:
        if value:
            return True

    return False
