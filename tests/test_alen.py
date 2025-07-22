from aioplus import alen, arange


POSITIVE_INTEGER = 2304


class TestAlen:
    """Tests for `aioplus.alen`."""

    async def test__alen(self) -> None:
        """Case: default behavior."""
        iterator = arange(POSITIVE_INTEGER)

        length = await alen(iterator)

        assert length == POSITIVE_INTEGER

    async def test__alen__empty(self) -> None:
        """Case: return `0` if empty."""
        iterator = arange(0)

        length = await alen(iterator)

        assert length == 0
