import pytest

from aioplus import arange, atail


class TestParameters:
    """Parameter tests."""

    async def test__aiterable(self) -> None:
        """Case: non-iterable."""
        with pytest.raises(TypeError):
            atail(None)

    async def test__n(self) -> None:
        """Case: non-integer."""
        with pytest.raises(TypeError):
            atail(arange(23), n="4")

    async def test__n__negative(self) -> None:
        """Case: `n < 0`."""
        with pytest.raises(ValueError, match="'n' must be non-negative"):
            atail(arange(23), n=-4)


class TestFunction:
    """Function tests."""

    async def test__atail(self) -> None:
        """Case: default usage."""
        aiterable = arange(23)

        tail = [num async for num in atail(aiterable, n=4)]

        assert tail == [19, 20, 21, 22]

    async def test__atail__empty(self) -> None:
        """Case: `len(...) == 0`."""
        aiterable = arange(0)

        tail = [num async for num in atail(aiterable, n=4)]

        assert not tail

    async def test__atail__less_than_n(self) -> None:
        """Case: `len(...) < n`."""
        aiterable = arange(2)

        tail = [num async for num in atail(aiterable, n=4)]

        assert tail == [0, 1]

    async def test__atail__n_is_zero(self) -> None:
        """Case: `n == 0`."""
        aiterable = arange(23)

        tail = [num async for num in atail(aiterable, n=0)]

        assert not tail
