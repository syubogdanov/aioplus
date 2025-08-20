import re

import pytest

from aioplus import amin, arange


class TestAmin:
    """Tests for `aioplus.alen`."""

    async def test__amin(self) -> None:
        """Case: default behavior."""
        aiterable = arange(23)

        smallest = await amin(aiterable)

        assert smallest == 0

    async def test__amin__empty(self) -> None:
        """Case: empty iterable."""
        aiterable = arange(0)

        with pytest.raises(ValueError, match=re.escape("amin(): empty iterable")):
            await amin(aiterable)

    async def test__amin__default(self) -> None:
        """Case: default value."""
        aiterable = arange(0)

        smallest = await amin(aiterable, default=23)

        assert smallest == 23

    async def test__amin__single_element(self) -> None:
        """Case: single element iterable."""
        aiterable = arange(1)

        smallest = await amin(aiterable)

        assert smallest == 0

    async def test__amin__key(self) -> None:
        """Case: key function provided."""
        aiterable = arange(5)

        smallest = await amin(aiterable, key=lambda x: -x)

        assert smallest == 4
