import re

import pytest

from aioplus import afirst, arange


class TestAfirst:
    """Tests for `aioplus.afirst`."""

    async def test__afirst(self) -> None:
        """Case: default behavior."""
        aiterator = arange(4, 23)

        value = await afirst(aiterator)

        assert value == 4

    async def test__afirst__empty(self) -> None:
        """Case: empty iterable."""
        aiterator = arange(0)

        with pytest.raises(IndexError, match=re.escape("afirst(): empty iterable")):
            await afirst(aiterator)

    async def test__afirst__default(self) -> None:
        """Case: default value is returned if iterable is empty."""
        aiterator = arange(0)

        value = await afirst(aiterator, default=23)

        assert value == 23
