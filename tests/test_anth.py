import re

import pytest

from aioplus import anth, arange


class TestParameters:
    """Parameter tests."""

    async def test__aiterable(self) -> None:
        """Case: non-iterable."""
        with pytest.raises(TypeError):
            await anth(None)

    async def test__n(self) -> None:
        """Case: non-integer."""
        with pytest.raises(TypeError):
            await anth(arange(23), n="4")

    async def test__n__negative(self) -> None:
        """Case: `n < 0`."""
        aiterable = arange(4)

        with pytest.raises(ValueError, match="'n' must be non-negative"):
            await anth(aiterable, n=-1)


class TestFunction:
    """Function tests."""

    async def test__anth(self) -> None:
        """Case: default usage."""
        aiterable = arange(23)

        value = await anth(aiterable, n=4)

        assert value == 4

    async def test__anth__out_of_bounds(self) -> None:
        """Case: `aiterable[n]` not exists."""
        aiterable = arange(4)

        with pytest.raises(IndexError, match=re.escape("'aiterable[n]' does not exist")):
            await anth(aiterable, n=23)

    async def test__anth__default(self) -> None:
        """Case: `default` provided."""
        aiterable = arange(4)

        value = await anth(aiterable, n=23, default=42)

        assert value == 42
