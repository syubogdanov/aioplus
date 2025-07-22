import pytest

from aioplus import arange


class TestArange:
    """Tests for `aioplus.arange`."""

    async def test__arange__one_parameter(self) -> None:
        """Case: one parameter."""
        nums = [num async for num in arange(10)]

        assert nums == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    async def test__arange__two_parameters(self) -> None:
        """Case: two parameters."""
        nums = [num async for num in arange(4, 10)]

        assert nums == [4, 5, 6, 7, 8, 9]

    async def test__arange__three_parameters(self) -> None:
        """Case: three parameters."""
        nums = [num async for num in arange(4, 23, 3)]

        assert nums == [4, 7, 10, 13, 16, 19, 22]

    async def test__arange__negative_step(self) -> None:
        """Case: negative step."""
        nums = [num async for num in arange(23, 4, -3)]

        assert nums == [23, 20, 17, 14, 11, 8, 5]

    async def test__arange__empty(self) -> None:
        """Case: empty range."""
        nums = [num async for num in arange(23, 4)]

        assert not nums

    async def test__arange__zero_step(self) -> None:
        """Case: zero step."""
        with pytest.raises(ValueError, match="'step' must not be zero"):
            [num async for num in arange(4, 23, 0)]

    async def test__arange__step_without_stop(self) -> None:
        """Case: step without stop."""
        with pytest.raises(ValueError, match="'step' is not specified but 'stop' is"):
            [num async for num in arange(4, None, 2)]  # type: ignore[call-overload]
