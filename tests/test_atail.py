import pytest

from aioplus import arange, atail


class TestAtail:
    """Tests for `aioplus.atail`."""

    async def test__atail(self) -> None:
        """Case: default usage."""
        aiterable = arange(23)

        tail = [num async for num in atail(aiterable, n=4)]

        assert tail == [19, 20, 21, 22]

    async def test__atail__empty(self) -> None:
        """Case: empty iterable."""
        aiterable = arange(0)

        tail = [num async for num in atail(aiterable, n=4)]

        assert not tail

    async def test__atail__less_than_n(self) -> None:
        """Case: less than `n` elements."""
        aiterable = arange(2)

        tail = [num async for num in atail(aiterable, n=4)]

        assert tail == [0, 1]

    async def test__atail__n_is_zero(self) -> None:
        """Case: `n` is zero."""
        aiterable = arange(23)

        tail = [num async for num in atail(aiterable, n=0)]

        assert not tail

    async def test__atail__n_is_negative(self) -> None:
        """Case: `n` is negative."""
        aiterable = arange(23)

        with pytest.raises(ValueError, match="'n' must be non-negative"):
            [num async for num in atail(aiterable, n=-4)]
