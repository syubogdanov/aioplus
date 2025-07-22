import json
import tomllib

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from tempfile import mkstemp

import pytest

from aioplus import awaitify


JSON = {"aioplus": "awaitify"}


@pytest.fixture
def path() -> Path:
    """Path to *JSON* file."""
    fd, path = mkstemp(suffix=".json")

    with open(fd, mode="w") as file:  # noqa: PTH123
        json.dump(JSON, file)

    return Path(path)


class TestAwaitify:
    """Tests for `aioplus.awaitify`."""

    async def test__awaitify(self, path: Path) -> None:
        """Case: default usage."""
        aexists = awaitify(path.exists)

        exists_flg = await aexists()

        assert exists_flg

    async def test__awaitify__args(self, path: Path) -> None:
        """Case: positional arguments are passed."""
        aload = awaitify(json.load)

        with path.open() as file:
            body = await aload(file)

        assert body == JSON

    async def test__awaitify__kwargs(self, path: Path) -> None:
        """Case: keyword arguments are passed."""
        aload = awaitify(json.load)

        with path.open() as file:
            body = await aload(fp=file)

        assert body == JSON

    async def test__awaitify__exception(self, path: Path) -> None:
        """Case: an exception is raised."""
        aload = awaitify(tomllib.load)

        with pytest.raises(tomllib.TOMLDecodeError), path.open(mode="rb") as file:
            await aload(file)

    async def test__awaitify__executor(self, path: Path) -> None:
        """Case: an executor is provided."""
        threads_created = 0

        def initializer() -> None:
            """Initialize the thread."""
            nonlocal threads_created
            threads_created += 1

        with ThreadPoolExecutor(initializer=initializer) as executor:
            aexists = awaitify(path.exists, executor=executor)

            exists_flg = await aexists()

            assert exists_flg
            assert threads_created == 1
