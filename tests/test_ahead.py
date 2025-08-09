import pytest

from aioplus import ahead, arange


class TestAhead:
    """Tests for `aioplus.ahead`."""

    async def test__ahead(self) -> None:
        """Case: default usage."""
        aiterable = arange(23)

        head = [num async for num in ahead(aiterable, n=4)]

        assert head == [0, 1, 2, 3]

    async def test__ahead__empty(self) -> None:
        """Case: empty iterable."""
        aiterable = arange(0)

        head = [num async for num in ahead(aiterable, n=4)]

        assert not head

    async def test__ahead__less_than_n(self) -> None:
        """Case: less than `n` elements."""
        aiterable = arange(2)

        head = [num async for num in ahead(aiterable, n=4)]

        assert head == [0, 1]

    async def test__ahead__n_is_zero(self) -> None:
        """Case: `n` is zero."""
        aiterable = arange(23)

        head = [num async for num in ahead(aiterable, n=0)]

        assert not head

    async def test__ahead__n_is_negative(self) -> None:
        """Case: `n` is negative."""
        aiterable = arange(23)

        with pytest.raises(ValueError, match="'n' must be non-negative"):
            [num async for num in ahead(aiterable, n=-4)]
