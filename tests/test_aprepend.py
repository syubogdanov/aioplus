from collections.abc import AsyncGenerator
from contextlib import aclosing

import pytest

from aioplus import aprepend, arange


class TestParameters:
    """Parameter tests."""

    def test__aiterable(self) -> None:
        """Case: non-iterable."""
        with pytest.raises(TypeError):
            aprepend(None, None)


class TestFunction:
    """Function tests."""

    async def test__aprepend(self) -> None:
        """Case: default usage."""
        aiterable = arange(1, 5)

        nums = [num async for num in aprepend(0, aiterable)]

        assert nums == [0, 1, 2, 3, 4]

    async def test__aprepend__empty(self) -> None:
        """Case: `len(...) == 0`."""
        aiterable = arange(0)

        nums = [num async for num in aprepend(42, aiterable)]

        assert nums == [42]

    async def test__aprepend__exception(self) -> None:
        """Case: exception."""

        async def generator() -> AsyncGenerator[int]:
            if True:
                raise RuntimeError
            yield 1

        async with aclosing(generator()) as aiterator:
            with pytest.raises(RuntimeError):
                [num async for num in aprepend(0, aiterator)]
