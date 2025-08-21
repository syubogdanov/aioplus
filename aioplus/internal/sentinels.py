from enum import Enum, auto


class Sentinel(Enum):
    """Just a sentinel.

    Notes
    -----
    * Inherits from `Enum` to be used as `typing.Literal`.
    """

    EMPTY = auto()
    UNSET = auto()
