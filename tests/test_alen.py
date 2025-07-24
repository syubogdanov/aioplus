from aioplus import alen, arange


POSITIVE_INTEGER = 2304


class TestAlen:
    """Tests for `aioplus.alen`."""

    async def test__alen(self) -> None:
        """Case: default behavior."""
        aiterator = arange(POSITIVE_INTEGER)

        length = await alen(aiterator)

        assert length == POSITIVE_INTEGER

    async def test__alen__empty(self) -> None:
        """Case: return `0` if empty."""
        aiterator = arange(0)

        length = await alen(aiterator)

        assert length == 0
