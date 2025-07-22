from aioplus import abatched, arange

import pytest


class TestAbatched:
    """Tests for `aioplus.abatched`."""

    async def test__abatched(self) -> None:
        """Case: default usage."""
        batches = [batch async for batch in abatched(arange(10), n=3)]

        assert batches == [(0, 1, 2), (3, 4, 5), (6, 7, 8), (9,)]

    async def test__abatched__empty(self) -> None:
        """Case: empty iterable."""
        batches = [batch async for batch in abatched(arange(0), n=3)]

        assert not batches

    async def test__abatched__negative_size(self) -> None:
        """Case: negative batch size."""
        with pytest.raises(ValueError):
            [batch async for batch in abatched(arange(10), n=-1)]

    async def test__abatched__zero_size(self) -> None:
        """Case: zero batch size."""
        with pytest.raises(ValueError):
            [batch async for batch in abatched(arange(10), n=0)]

    async def test__abatched__strict(self) -> None:
        """Case: strict mode."""
        with pytest.raises(ValueError):
            [batch async for batch in abatched(arange(10), n=3, strict=True)]
