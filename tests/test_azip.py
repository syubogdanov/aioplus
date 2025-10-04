import re

import pytest

from aioplus import arange, azip


class TestParameters:
    """Parameter tests."""

    def test__aiterables(self) -> None:
        """Case: non-iterable."""
        with pytest.raises(TypeError):
            azip(None)

    def test__aiterables__strict(self) -> None:
        """Case: non-iterable."""
        with pytest.raises(TypeError):
            azip(None, strict=23)


class TestFunction:
    """Function tests."""

    async def test__azip(self) -> None:
        """Case: default usage."""
        aiterables = [arange(4), arange(100, 104), arange(200, 204)]

        triplets = [triplet async for triplet in azip(*aiterables)]

        assert triplets == [(0, 100, 200), (1, 101, 201), (2, 102, 202), (3, 103, 203)]

    async def test__azip__strict(self) -> None:
        """Case: `strict=True`."""
        aiterables = [arange(4), arange(100, 104), arange(200, 205)]

        with pytest.raises(ValueError, match=re.escape("azip(): len(aiterable) differ")):
            [triplet async for triplet in azip(*aiterables, strict=True)]

    async def test__azip__empty(self) -> None:
        """Case: `len(...) == 0`."""
        results = [triplet async for triplet in azip()]

        assert not results
