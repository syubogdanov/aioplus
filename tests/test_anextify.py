from collections.abc import Generator

import pytest

from aioplus import CallerThreadExecutor, anextify


class TestParameters:
    """Parameter tests."""

    async def test__iterable(self) -> None:
        """Case: non-iterable."""
        with pytest.raises(TypeError):
            anextify(None)

    async def test__executor(self) -> None:
        """Case: non-executor."""
        with pytest.raises(TypeError):
            anextify([4], executor=23)


class TestFunction:
    """Function tests."""

    async def test__anextify(self) -> None:
        """Case: default usage."""
        iterable = [1, 2, 3, 4, 5]

        nums = [num async for num in anextify(iterable)]

        assert nums == [1, 2, 3, 4, 5]

    async def test__anextify__empty(self) -> None:
        """Case: `len(...) == 0`."""
        iterable: list[int] = []

        nums = [num async for num in anextify(iterable)]

        assert not nums

    async def test__anextify__exception(self) -> None:
        """Case: exception raised."""
        detail = "This is a mock exception!"

        def generator() -> Generator[int]:
            """Yield and raise an exception."""
            yield from range(23)
            raise ValueError(detail)

        with pytest.raises(ValueError, match=detail):
            [num async for num in anextify(generator())]

    async def test__anextify__executor(self) -> None:
        """Case: executor provided."""
        iterable = [1, 2, 3, 4, 5]

        aiterable = anextify(iterable, executor=CallerThreadExecutor())
        nums = [num async for num in aiterable]

        assert nums == [1, 2, 3, 4, 5]
