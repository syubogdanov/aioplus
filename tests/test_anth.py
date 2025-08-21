import re

import pytest

from aioplus import anth, arange


class TestAnth:
    """Tests for `aioplus.anth`."""

    async def test__anth(self) -> None:
        """Case: default behavior."""
        aiterable = arange(23)

        value = await anth(aiterable, n=4)

        assert value == 4

    async def test__anth__out_of_bounds(self) -> None:
        """Case: `n` is out of bounds."""
        aiterable = arange(4)

        with pytest.raises(IndexError, match=re.escape("'aiterable[n]' does not exist")):
            await anth(aiterable, n=23)

    async def test__anth__default(self) -> None:
        """Case: default value is returned when `n` is out of bounds."""
        aiterable = arange(4)

        value = await anth(aiterable, n=23, default=42)

        assert value == 42

    async def test__anth__negative_index(self) -> None:
        """Case: `n` is negative."""
        aiterable = arange(4)

        with pytest.raises(ValueError, match="'n' must be non-negative"):
            await anth(aiterable, n=-1)
