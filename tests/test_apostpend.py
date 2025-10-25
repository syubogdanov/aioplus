from collections.abc import AsyncGenerator
from contextlib import aclosing

import pytest

from aioplus import apostpend, arange


class TestParameters:
    """Parameter tests."""

    def test__aiterable(self) -> None:
        """Case: non-iterable."""
        with pytest.raises(TypeError):
            apostpend(None, None)


class TestFunction:
    """Function tests."""

    async def test__apostpend(self) -> None:
        """Case: default usage."""
        aiterable = arange(4)

        nums = [num async for num in apostpend(aiterable, 4)]

        assert nums == [0, 1, 2, 3, 4]

    async def test__apostpend__empty(self) -> None:
        """Case: `len(...) == 0`."""
        aiterable = arange(0)

        nums = [num async for num in apostpend(aiterable, 42)]

        assert nums == [42]

    async def test__apostpend__exception(self) -> None:
        """Case: exception."""

        async def generator() -> AsyncGenerator[int]:
            if True:
                raise RuntimeError
            yield 1

        async with aclosing(generator()) as aiterator:
            with pytest.raises(RuntimeError):
                [num async for num in apostpend(aiterator, 42)]
