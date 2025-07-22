import pytest

from aioplus import aislice, arange


class TestAislice:
    """Tests for `aioplus.aislice`."""

    async def test__aislice__stop(self) -> None:
        """Case: default usage."""
        nums = [num async for num in aislice(arange(10), 2, 8)]

        assert nums == [2, 3, 4, 5, 6, 7]

    async def test__aislice__start(self) -> None:
        """Case: start index specified."""
        nums = [num async for num in aislice(arange(10), 4, 7)]

        assert nums == [4, 5, 6]

    async def test__aislice__step(self) -> None:
        """Case: step specified."""
        nums = [num async for num in aislice(arange(10), 1, 9, 2)]

        assert nums == [1, 3, 5, 7]

    async def test__aislice__empty(self) -> None:
        """Case: empty iterable."""
        nums = [num async for num in aislice(arange(0), 2, 8)]

        assert not nums

    async def test__aislice__out_of_bounds(self) -> None:
        """Case: out of bounds indices."""
        nums = [num async for num in aislice(arange(10), 12, 15)]

        assert not nums

    async def test__aislice__negative_start(self) -> None:
        """Case: negative start index."""
        with pytest.raises(ValueError, match="'start' must be non-negative"):
            [num async for num in aislice(arange(10), -3, 8)]

    async def test__aislice__negative_stop(self) -> None:
        """Case: negative stop index."""
        with pytest.raises(ValueError, match="'stop' must be non-negative"):
            [num async for num in aislice(arange(10), 2, -2)]

    async def test__aislice__negative_step(self) -> None:
        """Case: negative step."""
        with pytest.raises(ValueError, match="'step' must be positive"):
            [num async for num in aislice(arange(10), 2, 8, -1)]

    async def test__aislice__zero_step(self) -> None:
        """Case: zero step."""
        with pytest.raises(ValueError, match="'step' must be positive"):
            [num async for num in aislice(arange(10), 2, 8, 0)]

    async def test__aislice__step_without_stop(self) -> None:
        """Case: step without stop."""
        with pytest.raises(ValueError, match="'step' is not specified but 'stop' is"):
            [num async for num in aislice(arange(10), 2, None, 2)]  # type: ignore[call-overload]
