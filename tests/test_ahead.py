import pytest

from aioplus import ahead, arange


class TestParameters:
    """Parameter tests."""

    def test__aiterable(self) -> None:
        """Case: non-iterable."""
        with pytest.raises(TypeError):
            ahead(None)

    def test__n__negative(self) -> None:
        """Case: `n < 0`."""
        with pytest.raises(ValueError, match="'n' must be non-negative"):
            ahead(arange(23), n=-4)


class TestFunction:
    """Function tests."""

    async def test__ahead(self) -> None:
        """Case: default usage."""
        aiterable = arange(23)

        head = [num async for num in ahead(aiterable, n=4)]

        assert head == [0, 1, 2, 3]

    async def test__ahead__empty(self) -> None:
        """Case: `len(...) == 0`."""
        aiterable = arange(0)

        head = [num async for num in ahead(aiterable, n=4)]

        assert not head

    async def test__ahead__less_than_n(self) -> None:
        """Case: `len(...) < n`."""
        aiterable = arange(2)

        head = [num async for num in ahead(aiterable, n=4)]

        assert head == [0, 1]

    async def test__ahead__n_is_zero(self) -> None:
        """Case: `n == 0`."""
        aiterable = arange(23)

        head = [num async for num in ahead(aiterable, n=0)]

        assert not head
