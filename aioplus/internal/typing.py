from abc import abstractmethod
from typing import Protocol, runtime_checkable


@runtime_checkable
class SupportsBool(Protocol):
    """An ABC with one abstract method `__bool__`."""

    @abstractmethod
    def __bool__(self) -> bool:
        """Cast to `bool`."""
