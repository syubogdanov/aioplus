from collections.abc import AsyncIterable

from aioplus.internal.typing import SupportsBool


async def aany(aiterable: AsyncIterable[SupportsBool], /) -> bool:
    """
    Return ``True`` if any element of the async iterable evaluates to ``True``.

    This is an asynchronous equivalent of the built-in :func:`any`.

    Parameters
    ----------
    aiterable : AsyncIterable of SupportsBool
        An asynchronous iterable where each item must support boolean evaluation,
        i.e., implement the ``__bool__`` method.

    Returns
    -------
    bool
        ``True`` if any element evaluates to ``True``.
        ``False`` if all elements evaluate to ``False``, or if the iterable is empty.

    Notes
    -----
    - This function short-circuits: evaluation stops at the first item that evaluates to ``True``.
    - If ``aiterable`` is empty, ``False`` is returned by definition (vacuous falsity).

    See Also
    --------
    builtins.any : The synchronous version for regular iterables.
    """
    async for value in aiterable:
        if bool(value):
            return True
    return False
