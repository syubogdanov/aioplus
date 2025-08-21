import json
import tomllib

from pathlib import Path
from tomllib import TOMLDecodeError

import pytest

from aioplus import CallerThreadExecutor, awaitify


JSON = {"aioplus": "awaitify"}


@pytest.fixture
def path(tempfile: Path) -> Path:
    """Path to *JSON* file."""
    with tempfile.open(mode="w") as file:
        json.dump(JSON, file)
    return tempfile


class TestAwaitify:
    """Tests for `aioplus.awaitify`."""

    async def test__awaitify(self, path: Path) -> None:
        """Case: default usage."""
        aexists = awaitify(path.exists)

        exists_flg = await aexists()

        assert exists_flg

    async def test__awaitify__args(self, path: Path) -> None:
        """Case: positional arguments."""
        aload = awaitify(json.load)

        with path.open() as file:
            obj = await aload(file)

        assert obj == JSON

    async def test__awaitify__kwargs(self, path: Path) -> None:
        """Case: keyword arguments."""
        aload = awaitify(json.load)

        with path.open() as file:
            obj = await aload(fp=file)

        assert obj == JSON

    async def test__awaitify__exception(self, path: Path) -> None:
        """Case: an exception is raised."""
        aload = awaitify(tomllib.load)

        with path.open(mode="rb") as file, pytest.raises(TOMLDecodeError):
            await aload(file)

    async def test__awaitify__executor(self, path: Path) -> None:
        """Case: executor provided."""
        executor = CallerThreadExecutor()
        aexists = awaitify(path.exists, executor=executor)

        exists_flg = await aexists()

        assert exists_flg
