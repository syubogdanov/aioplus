from collections.abc import AsyncIterator
from typing import Protocol, TypeVar, runtime_checkable


T_co = TypeVar("T_co", covariant=True)
T_contra = TypeVar("T_contra", contravariant=True)


@runtime_checkable
class SupportsAdd(Protocol[T_contra, T_co]):
    """An ABC with one abstract method `__add__`."""

    def __add__(self, x: T_contra, /) -> T_co:
        """Perform addition operation."""


@runtime_checkable
class SupportsBool(Protocol):
    """An ABC with one abstract method `__bool__`."""

    def __bool__(self) -> bool:
        """Perform boolean conversion."""


@runtime_checkable
class SupportsRAdd(Protocol[T_contra, T_co]):
    """An ABC with one abstract method `__radd__`."""

    def __radd__(self, x: T_contra, /) -> T_co:
        """Perform reverse addition operation."""


@runtime_checkable
class SupportsDunderLT(Protocol[T_contra]):
    """An ABC with one abstract method `__lt__`."""

    def __lt__(self, other: T_contra, /) -> bool:
        """Perform less-than comparison."""


@runtime_checkable
class SupportsDunderGT(Protocol[T_contra]):
    """An ABC with one abstract method `__gt__`."""

    def __gt__(self, other: T_contra, /) -> bool:
        """Perform greater-than comparison."""


@runtime_checkable
class SupportsAclose(Protocol):
    """An ABC with one abstract method `aclose`."""

    async def aclose(self) -> object:
        """Close the object."""


@runtime_checkable
class AcloseableIterator(AsyncIterator[T_co], SupportsAclose, Protocol[T_co]):
    """An ABC that implements three abstract methods: `__aiter__`, `__anext__` and `aclose`."""
