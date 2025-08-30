import pytest

from aioplus import arange, awindowed


class TestParameters:
    """Parameter tests."""

    def test__aiterable(self) -> None:
        """Case: non-iterable."""
        with pytest.raises(TypeError):
            awindowed(None)

    def test__n(self) -> None:
        """Case: non-integer 'n'."""
        with pytest.raises(TypeError):
            awindowed(arange(23), n="4")

    def test__n__negative(self) -> None:
        """Case: `n < 0`."""
        with pytest.raises(ValueError, match="'n' must be positive"):
            awindowed(arange(23), n=-4)

    def test__n__zero(self) -> None:
        """Case: `n == 0`."""
        with pytest.raises(ValueError, match="'n' must be positive"):
            awindowed(arange(23), n=0)


class TestFunction:
    """Function tests."""

    async def test__awindowed__singles(self) -> None:
        """Case: `n == 1`."""
        aiterable = arange(5)

        windows = [window async for window in awindowed(aiterable, n=1)]

        assert windows == [(0,), (1,), (2,), (3,), (4,)]

    async def test__awindowed__pairs(self) -> None:
        """Case: `n == 2`."""
        aiterable = arange(5)

        windows = [window async for window in awindowed(aiterable, n=2)]

        assert windows == [(0, 1), (1, 2), (2, 3), (3, 4)]

    async def test__awindowed__triplets(self) -> None:
        """Case: `n == 3`."""
        aiterable = arange(5)

        windows = [window async for window in awindowed(aiterable, n=3)]

        assert windows == [(0, 1, 2), (1, 2, 3), (2, 3, 4)]

    async def test__awindowed__empty(self) -> None:
        """Case: `len(...) == 0`."""
        aiterable = arange(0)

        windows = [window async for window in awindowed(aiterable, n=1)]

        assert not windows

    async def test__awindowed__less_elements_than_window_size(self) -> None:
        """Case: `len(...) < n`."""
        aiterable = arange(4)

        windows = [window async for window in awindowed(aiterable, n=23)]

        assert not windows
