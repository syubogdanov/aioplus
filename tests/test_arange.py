import pytest

from aioplus import arange


class TestParameters:
    """Parameter tests."""

    async def test__aiterable(self) -> None:
        """Case: non-iterable."""
        with pytest.raises(TypeError):
            arange(None)

    async def test__start(self) -> None:
        """Case: non-integer."""
        with pytest.raises(TypeError):
            arange("0")

    async def test__stop(self) -> None:
        """Case: non-integer."""
        with pytest.raises(TypeError):
            arange(0, "4")

    async def test__step(self) -> None:
        """Case: non-integer."""
        with pytest.raises(TypeError):
            arange(0, 4, "23")

    async def test__step__zero(self) -> None:
        """Case: `step == 0`."""
        with pytest.raises(ValueError, match="'step' must not be zero"):
            arange(4, 23, 0)

    async def test__arange__step_without_stop(self) -> None:
        """Case: `step` without `stop`."""
        with pytest.raises(ValueError, match="'step' is not specified but 'stop' is"):
            arange(4, None, 23)


class TestFunction:
    """Function tests."""

    async def test__arange__stop(self) -> None:
        """Case: `stop` provided."""
        aiterable = arange(10)

        nums = [num async for num in aiterable]

        assert nums == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    async def test__arange__start_and_stop(self) -> None:
        """Case: `start` and `stop` provided."""
        aiterable = arange(4, 10)

        nums = [num async for num in aiterable]

        assert nums == [4, 5, 6, 7, 8, 9]

    async def test__arange__all_parameters(self) -> None:
        """Case: `start`, `stop`, and `step` provided."""
        aiterable = arange(4, 23, 3)

        nums = [num async for num in aiterable]

        assert nums == [4, 7, 10, 13, 16, 19, 22]

    async def test__arange__negative_step(self) -> None:
        """Case: `step < 0`."""
        aiterable = arange(23, 4, -3)

        nums = [num async for num in aiterable]

        assert nums == [23, 20, 17, 14, 11, 8, 5]

    async def test__arange__empty(self) -> None:
        """Case: `len(...) == 0`."""
        aiterable = arange(23, 4)

        nums = [num async for num in aiterable]

        assert not nums
