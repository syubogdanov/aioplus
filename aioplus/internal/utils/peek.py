from collections.abc import AsyncIterator
from dataclasses import dataclass
from typing import TypeVar


T = TypeVar("T")


@dataclass
class MaybePeek


def one(aiterator: AsyncIterator[T]) -> T:
    """Peek the next element."""
    return cast(T, aiterator._peek_one())
