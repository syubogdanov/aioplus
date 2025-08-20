import re

import pytest

from aioplus import amax, arange


class TestAmax:
    """Tests for `aioplus.amax`."""

    async def test__amax(self) -> None:
        """Case: default behavior."""
        aiterable = arange(23)

        largest = await amax(aiterable)

        assert largest == 22

    async def test__amax__empty(self) -> None:
        """Case: empty iterable."""
        aiterable = arange(0)

        with pytest.raises(ValueError, match=re.escape("amax(): empty iterable")):
            await amax(aiterable)

    async def test__amax__default(self) -> None:
        """Case: default value."""
        aiterable = arange(0)

        largest = await amax(aiterable, default=23)

        assert largest == 23

    async def test__amax__single_element(self) -> None:
        """Case: single element iterable."""
        aiterable = arange(1)

        largest = await amax(aiterable)

        assert largest == 0

    async def test__amax__key(self) -> None:
        """Case: key function provided."""
        aiterable = arange(5)

        largest = await amax(aiterable, key=lambda x: -x)

        assert largest == 0
