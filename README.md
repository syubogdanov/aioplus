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

#### *afirst*

```python
import asyncio

from aioplus import afirst

async def main() -> None:
    """Run the program."""
    coroutines = [
        asyncio.sleep(delay=3.0, result="third"),
        asyncio.sleep(delay=1.0, result="first"),
        asyncio.sleep(delay=2.0, result="second"),
    ]

    tasks = [asyncio.create_task(coroutine) for coroutine in coroutines]
    first, pending = await afirst(tasks)

    ...

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
