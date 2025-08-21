from collections.abc import Callable
from concurrent.futures import Executor
from typing import ParamSpec, TypeVar


P = ParamSpec("P")
R = TypeVar("R")


class CurrentThreadExecutor(Executor):
    """An executor that uses the current thread.

    Examples
    --------
    >>> executor = CurrentThreadExecutor()
    >>> iterable = [1, 2, 3, 4, 5, 6, 7, 8]
    >>> aiterable = anextify(iterable, executor=executor)
    >>> [num async for num in aiterable]
    [1, 2, 3, 4, 5, 6, 7, 8]

    See Also
    --------
    :class:`concurrent.futures.Executor`
    """
