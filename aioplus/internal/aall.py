from collections.abc import AsyncIterable

from aioplus.internal.typing import SupportsBool


async def aall(aiterable: AsyncIterable[SupportsBool], /) -> bool:
    """
    Return :obj:`True` if all elements of the async iterable evaluate to :obj:`True`.

    Parameters
    ----------
    aiterable : AsyncIterable of SupportsBool
        An asynchronous iterable where each item must support boolean evaluation,
        i.e., implement the :meth:`__bool__` method.

    Returns
    -------
    bool
        :obj:`True` if all elements evaluate to :obj:`True`, or if the iterable is empty.
        :obj:`False` if any element evaluates to :obj:`False`.

    Notes
    -----
    - Evaluation stops at the first item that evaluates to :obj:`False`.
    - If ``aiterable`` is empty, :obj:`True` is returned by definition (vacuous truth).

    See Also
    --------
    :func:`builtins.all` : The synchronous version for regular iterables.
    """
    async for value in aiterable:
        if not bool(value):
            return False
    return True
