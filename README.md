# aioplus

[![PyPI Version][shields/pypi/version]][pypi/homepage]
[![PyPI Downloads][shields/pypi/downloads]][pypi/homepage]
[![License][shields/pypi/license]][github/license]
[![Python Version][shields/python/version]][pypi/homepage]

> [!WARNING]
> The library is in the pre-alpha stage. Bugs may exist!

## Getting Started

### Installation

The library is available as [`aioplus`][pypi/homepage] on PyPI:

```shell
pip install aioplus
```

### Usage

For more, see the [documentation][docs/aioplus].

#### *aall*

```python
import asyncio

from aioplus import aall, arange

async def main() -> None:
    """Run the program."""
    only_odd = await aall(
        num % 2 != 0
        async for num in arange(2304)
    )

if __name__ == "__main__":
    asyncio.run(main())
```

#### *aany*

```python
import asyncio

from aioplus import aany, arange

async def main() -> None:
    """Run the program."""
    has_odd = await aany(
        num % 2 != 0
        async for num in arange(2304)
    )

if __name__ == "__main__":
    asyncio.run(main())
```

#### *abatched*

```python
import asyncio

from aioplus import abatched, arange

async def main() -> None:
    """Run the program."""
    async for batch in abatched(arange(23), n=4):
        print(batch)

if __name__ == "__main__":
    asyncio.run(main())
```

#### *aislice*

```python
import asyncio

from aioplus import aislice, arange

async def main() -> None:
    """Run the program."""
    async for num in aislice(arange(23), 4):
        print(num)

if __name__ == "__main__":
    asyncio.run(main())
```

#### *alen*

```python
import asyncio

from aioplus import alen, arange

async def main() -> None:
    """Run the program."""
    aiterable = arange(2304)
    length = await alen(aiterable)
    print(f"len(aiterable) == {length}")

if __name__ == "__main__":
    asyncio.run(main())
```

#### *arange*

```python
import asyncio

from aioplus import arange

async def main() -> None:
    """Run the program."""
    async for num in arange(2304):
        print(num)

if __name__ == "__main__":
    asyncio.run(main())
```

#### *areversed*

```python
import asyncio

from aioplus import arange, areversed

async def main() -> None:
    """Run the program."""
    async for num in areversed(arange(2304)):
        print(num)

if __name__ == "__main__":
    asyncio.run(main())
```

#### *awaitify*

```python
import asyncio

from aioplus import awaitify

def func(num: int) -> None:
    """Print the number."""
    print(f"Num: {num}")

async def main() -> None:
    """Run the program."""
    afunc = awaitify(func)
    await afunc(num=2304)

if __name__ == "__main__":
    asyncio.run(main())
```

#### *ayield*

```python
import asyncio

from aioplus import ayield

async def worker(name: str) -> None:
    """Print the numbers."""
    for num in range(2304):
        print(f"{name}: {num}")
        await ayield()

async def main() -> None:
    """Run the program."""
    workers = [worker("A"), worker("B")]
    await asyncio.gather(*workers)

if __name__ == "__main__":
    asyncio.run(main())
```

## License

MIT License, Copyright (c) 2025 Sergei Y. Bogdanov. See [LICENSE][github/license] file.

<!-- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- -->

[docs/aioplus]: https://aioplus.readthedocs.io/

[github/license]: https://github.com/syubogdanov/aioplus/tree/main/LICENSE

[pypi/homepage]: https://pypi.org/project/aioplus/

[shields/pypi/downloads]: https://img.shields.io/pypi/dm/aioplus.svg?color=green
[shields/pypi/license]: https://img.shields.io/pypi/l/aioplus.svg?color=green
[shields/pypi/version]: https://img.shields.io/pypi/v/aioplus.svg?color=green
[shields/python/version]: https://img.shields.io/pypi/pyversions/aioplus.svg?color=green
