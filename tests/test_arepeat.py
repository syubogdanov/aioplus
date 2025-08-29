import pytest

from aioplus import ahead, arepeat


class TestParameters:
    """Parameter tests."""

    async def test__times(self) -> None:
        """Case: non-integer."""
        with pytest.raises(TypeError):
            arepeat(4, times="23")

    async def test__times__negative(self) -> None:
        """Case: `times < 0`."""
        with pytest.raises(ValueError, match="'times' must be non-negative"):
            arepeat(23, times=-4)


class TestFunction:
    """Function tests."""

    async def test__arepeat(self) -> None:
        """Case: default usage."""
        nums = [num async for num in arepeat(23, times=4)]

        assert nums == [23, 23, 23, 23]

    async def test__arepeat__zero_times(self) -> None:
        """Case: `times == 0`."""
        nums = [num async for num in arepeat(23, times=0)]

        assert not nums

    async def test__arepeat__infinite(self) -> None:
        """Case: infinite repetition."""
        nums = [num async for num in ahead(arepeat(23), n=4)]

        assert nums == [23, 23, 23, 23]
