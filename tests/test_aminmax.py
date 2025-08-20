import re

import pytest

from aioplus import aminmax, arange


class TestAminmax:
    """Tests for `aioplus.aminmax`."""

    async def test__aminmax(self) -> None:
        """Case: default behavior."""
        aiterable = arange(23)

        smallest, largest = await aminmax(aiterable)

        assert smallest == 0
        assert largest == 22

    async def test__aminmax__empty(self) -> None:
        """Case: empty iterable."""
        aiterable = arange(0)

        with pytest.raises(ValueError, match=re.escape("aminmax(): empty iterable")):
            await aminmax(aiterable)

    async def test__aminmax__default(self) -> None:
        """Case: default value."""
        aiterable = arange(0)

        smallest, largest = await aminmax(aiterable, default=(23, 4))

        assert smallest == 23
        assert largest == 4

    async def test__aminmax__single_element(self) -> None:
        """Case: single element iterable."""
        aiterable = arange(1)

        smallest, largest = await aminmax(aiterable)

        assert smallest == 0
        assert largest == 0

    async def test__aminmax__key(self) -> None:
        """Case: key function provided."""
        aiterable = arange(5)

        smallest, largest = await aminmax(aiterable, key=lambda x: -x)

        assert smallest == 4
        assert largest == 0
