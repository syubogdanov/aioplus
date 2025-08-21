from collections.abc import Generator
from contextlib import closing

import pytest

from aioplus import CallerThreadExecutor, anextify


class TestAnextify:
    """Tests for `aioplus.anextify`."""

    async def test__anextify(self) -> None:
        """Case: default usage."""
        iterable = [1, 2, 3, 4, 5]

        nums = [num async for num in anextify(iterable)]

        assert nums == [1, 2, 3, 4, 5]

    async def test__anextify__empty(self) -> None:
        """Case: empty iterable."""
        iterable: list[int] = []

        nums = [num async for num in anextify(iterable)]

        assert not nums

    async def test__anextify__exception(self) -> None:
        """Case: an exception raised."""
        detail = "This is a mock exception!"

        def generator() -> Generator[int]:
            """Yield and raise an exception."""
            yield from range(23)
            raise ValueError(detail)

        with closing(generator()) as iterable, pytest.raises(ValueError, match=detail):
            [num async for num in anextify(iterable)]

    async def test__anextify__executor(self) -> None:
        """Case: executor provided."""
        iterable = [1, 2, 3, 4, 5]

        executor = CallerThreadExecutor()
        aiterable = anextify(iterable, executor=executor)

        nums = [num async for num in aiterable]

        assert nums == [1, 2, 3, 4, 5]
