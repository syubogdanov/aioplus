from collections.abc import AsyncIterable

from aioplus.internal.typing import SupportsBool


async def aall(aiterable: AsyncIterable[SupportsBool], /) -> bool:
    """
    Return ``True`` if all elements of the async iterable evaluate to ``True``.

    This is an asynchronous equivalent of the built-in :func:`all`.

    Parameters
    ----------
    aiterable : AsyncIterable of SupportsBool
        An asynchronous iterable where each item must support boolean evaluation,
        i.e., implement the ``__bool__`` method.

    Returns
    -------
    bool
        ``True`` if all elements evaluate to ``True``, or if the iterable is empty.
        ``False`` if any element evaluates to ``False``.

    Notes
    -----
    - This function short-circuits: evaluation stops at the first item that evaluates to ``False``.
    - If ``aiterable`` is empty, ``True`` is returned by definition (vacuous truth).

    See Also
    --------
    builtins.all : The synchronous version for regular iterables.
    """
    async for value in aiterable:
        if not bool(value):
            return False
    return True
