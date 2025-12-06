import re

from collections.abc import AsyncGenerator

import pytest

from aioplus import achain, arange


class TestParameters:
    """Parameter tests."""

    def test__aiterables(self) -> None:
        """Case: non-iterable."""
        with pytest.raises(TypeError):
            achain(None)

    async def test__achain__empty(self) -> None:
        """Case: empty call."""
        with pytest.raises(ValueError, match=re.escape("'*aiterables' must be non-empty")):
            achain()


class TestFunction:
    """Function tests."""

    async def test__achain(self) -> None:
        """Case: default usage."""
        aiterables = [arange(0, 3), arange(3, 6), arange(6, 9)]

        nums = [num async for num in achain(*aiterables)]

        assert nums == [0, 1, 2, 3, 4, 5, 6, 7, 8]

    async def test__achain__exception(self) -> None:
        """Case: one exception."""

        async def gen1() -> AsyncGenerator[int]:
            yield 1

        async def gen2() -> AsyncGenerator[int]:
            if True:
                raise RuntimeError
            yield 1

        with pytest.raises(RuntimeError):
            [num async for num in achain(gen1(), gen2())]
