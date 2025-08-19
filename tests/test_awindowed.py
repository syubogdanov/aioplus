import pytest

from aioplus import arange, awindowed


class TestAwindowed:
    """Tests for `aioplus.awindowed`."""

    async def test__awindowed__singles(self) -> None:
        """Case: default usage."""
        windows = [window async for window in awindowed(arange(5), n=1)]

        assert windows == [(0,), (1,), (2,), (3,), (4,)]

    async def test__awindowed__pairs(self) -> None:
        """Case: default usage."""
        windows = [window async for window in awindowed(arange(5), n=2)]

        assert windows == [(0, 1), (1, 2), (2, 3), (3, 4)]

    async def test__awindowed__triplets(self) -> None:
        """Case: default usage."""
        windows = [window async for window in awindowed(arange(5), n=3)]

        assert windows == [(0, 1, 2), (1, 2, 3), (2, 3, 4)]

    async def test__awindowed__empty(self) -> None:
        """Case: empty iterable."""
        windows = [window async for window in awindowed(arange(0), n=1)]

        assert not windows

    async def test__awindowed__less_elements_than_window_size(self) -> None:
        """Case: single element iterable."""
        windows = [window async for window in awindowed(arange(4), n=23)]

        assert not windows

    async def test__awindowed__negative_window_size(self) -> None:
        """Case: negative window size."""
        with pytest.raises(ValueError, match="'n' must be positive"):
            [window async for window in awindowed(arange(23), n=-4)]

    async def test__awindowed__zero_window_size(self) -> None:
        """Case: zero window size."""
        with pytest.raises(ValueError, match="'n' must be positive"):
            [window async for window in awindowed(arange(23), n=0)]
