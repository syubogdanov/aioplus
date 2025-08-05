import pytest

from aioplus import anth, arange


class TestAnth:
    """Tests for `aioplus.anth`."""

    async def test__anth(self) -> None:
        """Case: default behavior."""
        aiterator = arange(23)

        value = await anth(aiterator, n=4)

        assert value == 4

    async def test__anth__out_of_bounds(self) -> None:
        """Case: `n` is out of bounds."""
        aiterator = arange(4)

        with pytest.raises(IndexError, match="The iterable contains fewer than 'n' items"):
            await anth(aiterator, n=23)

    async def test__anth__default(self) -> None:
        """Case: default value is returned when `n` is out of bounds."""
        aiterator = arange(4)

        value = await anth(aiterator, n=23, default=42)

        assert value == 42
