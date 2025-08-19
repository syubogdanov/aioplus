import re

import pytest

from aioplus import alast, arange


class TestAlast:
    """Tests for `aioplus.alast`."""

    async def test__alast(self) -> None:
        """Case: default behavior."""
        aiterator = arange(4, 23)

        value = await alast(aiterator)

        assert value == 22

    async def test__alast__empty(self) -> None:
        """Case: empty iterable."""
        aiterator = arange(0)

        with pytest.raises(IndexError, match=re.escape("alast(): empty iterable")):
            await alast(aiterator)

    async def test__alast__default(self) -> None:
        """Case: default value is returned if iterable is empty."""
        aiterator = arange(0)

        value = await alast(aiterator, default=23)

        assert value == 23
