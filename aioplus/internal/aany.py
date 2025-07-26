from collections.abc import AsyncIterable

from aioplus.internal.typing import SupportsBool


async def aany(aiterable: AsyncIterable[SupportsBool], /) -> bool:
    """
    Return :obj:`True` if any element of the async iterable evaluates to :obj:`True`.

    Parameters
    ----------
    aiterable : AsyncIterable of SupportsBool
        An asynchronous iterable where each item must support boolean evaluation,
        i.e., implement the :meth:`object.__bool__` method.

    Returns
    -------
    :class:`bool`
        :obj:`True` if any element evaluates to :obj:`True`.
        :obj:`False` if all elements evaluate to :obj:`False`, or if the iterable is empty.

    Notes
    -----
    - Evaluation stops at the first item that evaluates to :obj:`True`.
    - If ``aiterable`` is empty, :obj:`False` is returned by definition (vacuous falsity).

    See Also
    --------
    :func:`any`
    """
    async for value in aiterable:
        if bool(value):
            return True
    return False
