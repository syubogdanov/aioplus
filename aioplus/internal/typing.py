from abc import abstractmethod
from typing import Literal, Protocol, TypeVar, runtime_checkable


T_co = TypeVar("T_co", covariant=True)
T_contra = TypeVar("T_contra", contravariant=True)


LiteralPositiveInteger = Literal[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
LiteralNegativeInteger = Literal[-1, -2, -3, -4, -5, -6, -7, -8, -9, -10, -11, -12, -13, -14, -15]

LiteralInteger = LiteralNegativeInteger | Literal[0] | LiteralPositiveInteger


@runtime_checkable
class SupportsAdd(Protocol[T_contra, T_co]):
    """An ABC with one abstract method `__add__`."""

    @abstractmethod
    def __add__(self, x: T_contra, /) -> T_co:
        """Perform addition operation."""


@runtime_checkable
class SupportsBool(Protocol):
    """An ABC with one abstract method `__bool__`."""

    @abstractmethod
    def __bool__(self) -> bool:
        """Perform boolean conversion."""


@runtime_checkable
class SupportsRAdd(Protocol[T_contra, T_co]):
    """An ABC with one abstract method `__radd__`."""

    @abstractmethod
    def __radd__(self, x: T_contra, /) -> T_co:
        """Perform reverse addition operation."""
