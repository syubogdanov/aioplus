from aioplus.internal.arange import arange
from aioplus.internal.awaitify import awaitify
from aioplus.internal.ayield import ayield


__author__ = "Sergei Y. Bogdanov <syubogdanov@outlook.com>"
__version__ = "0.0.0"

__all__: list[str] = ["arange", "awaitify", "ayield"]


arange.__module__ = "aioplus"
awaitify.__module__ = "aioplus"
ayield.__module__ = "aioplus"
