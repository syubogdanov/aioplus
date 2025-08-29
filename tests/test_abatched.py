import re

import pytest

from aioplus import abatched, arange


class TestParameters:
    """Parameter tests."""

    async def test__aiterable(self) -> None:
        """Case: non-iterable."""
        with pytest.raises(TypeError):
            await abatched(None, n=23)

    async def test__n(self) -> None:
        """Case: non-integer."""
        with pytest.raises(TypeError):
            await abatched(arange(0), n=None)

    async def test__n__zero(self) -> None:
        """Case: zero batch size."""
        with pytest.raises(ValueError, match="'n' must be positive"):
            await abatched(arange(0), n=0)

    async def test__n__negative(self) -> None:
        """Case: negative batch size."""
        with pytest.raises(ValueError, match="'n' must be positive"):
            await abatched(arange(0), n=-1)

    async def test__strict(self) -> None:
        """Case: non-boolean."""
        with pytest.raises(TypeError):
            await abatched(arange(0), n=23, strict=None)


class TestFunction:
    """Function tests."""

    async def test__abatched(self) -> None:
        """Case: default usage."""
        aiterable = arange(10)

        batches = [batch async for batch in abatched(aiterable, n=3)]

        assert batches == [(0, 1, 2), (3, 4, 5), (6, 7, 8), (9,)]

    async def test__abatched__empty(self) -> None:
        """Case: empty iterable."""
        aiterable = arange(0)

        batches = [batch async for batch in abatched(aiterable, n=4)]

        assert not batches

    async def test__abatched__strict(self) -> None:
        """Case: `strict` provided."""
        aiterable = arange(23)

        with pytest.raises(ValueError, match=re.escape("abatched(): incomplete batch")):
            [batch async for batch in abatched(aiterable, n=4, strict=True)]
