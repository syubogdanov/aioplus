import pytest

from aioplus import aislice, arange


class TestParameters:
    """Parameter tests."""

    async def test__aiterable(self) -> None:
        """Case: non-iterable."""
        with pytest.raises(TypeError):
            aislice(None, 23)

    async def test__stop(self) -> None:
        """Case: non-integer."""
        with pytest.raises(TypeError):
            aislice(arange(2304), "23")

    async def test__start(self) -> None:
        """Case: non-integer."""
        with pytest.raises(TypeError):
            aislice(arange(10), 23, "4")

    async def test__step(self) -> None:
        """Case: non-integer."""
        with pytest.raises(TypeError):
            aislice(arange(10), 0, 4, "23")

    async def test__stop__negative(self) -> None:
        """Case: `stop < 0`."""
        with pytest.raises(ValueError, match="'stop' must be non-negative"):
            aislice(arange(23), -4)

    async def test__start__negative(self) -> None:
        """Case: `start < 0`."""
        with pytest.raises(ValueError, match="'start' must be non-negative"):
            aislice(arange(23), -4, 23)

    async def test__aislice__negative_step(self) -> None:
        """Case: `step < 0`."""
        with pytest.raises(ValueError, match="'step' must be positive"):
            aislice(arange(23), 4, 23, -1)

    async def test__aislice__zero_step(self) -> None:
        """Case: `step == 0`."""
        with pytest.raises(ValueError, match="'step' must be positive"):
            aislice(arange(23), 4, 23, 0)

    async def test__aislice__step_without_stop(self) -> None:
        """Case: `step` without `stop`."""
        with pytest.raises(ValueError, match="'step' is not specified but 'stop' is"):
            aislice(arange(23), 4, None, 23)


class TestFunction:
    """Function tests."""

    async def test__aislice__stop(self) -> None:
        """Case: default usage."""
        aiterable = arange(23)

        nums = [num async for num in aislice(aiterable, 4)]

        assert nums == [0, 1, 2, 3]

    async def test__aislice__start(self) -> None:
        """Case: `start` provided."""
        aiterable = arange(23)

        nums = [num async for num in aislice(aiterable, 4, 7)]

        assert nums == [4, 5, 6]

    async def test__aislice__step(self) -> None:
        """Case: `step` provided."""
        nums = [num async for num in aislice(arange(23), 4, 23, 4)]

        assert nums == [4, 8, 12, 16, 20]

    async def test__aislice__empty(self) -> None:
        """Case: `len(...) == 0`."""
        aiterable = arange(0)

        nums = [num async for num in aislice(aiterable, 4, 23)]

        assert not nums

    async def test__aislice__out_of_bounds(self) -> None:
        """Case: `aiterable[start]` not exists."""
        aiterable = arange(4)

        nums = [num async for num in aislice(aiterable, 4, 23)]

        assert not nums
