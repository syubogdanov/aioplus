import re

import pytest

from aioplus import alast, arange


class TestParameters:
    """Parameter tests."""

    async def test__aiterable(self) -> None:
        """Case: non-iterable."""
        with pytest.raises(TypeError):
            await alast(None)


class TestFunction:
    """Function tests."""

    async def test__alast(self) -> None:
        """Case: default usage."""
        aiterable = arange(4, 23)

        value = await alast(aiterable)

        assert value == 22

    async def test__alast__empty(self) -> None:
        """Case: `len(...) == 0`."""
        aiterable = arange(0)

        with pytest.raises(IndexError, match=re.escape("alast(): empty iterable")):
            await alast(aiterable)

    async def test__alast__default(self) -> None:
        """Case: `default` provided."""
        aiterable = arange(0)

        value = await alast(aiterable, default=23)

        assert value == 23
