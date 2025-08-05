# aioplus

[![PyPI Version][shields/pypi/version]][pypi/homepage]
[![PyPI Downloads][shields/pypi/downloads]][pypi/homepage]
[![License][shields/pypi/license]][github/license]
[![Python Version][shields/python/version]][pypi/homepage]
[![Documentation][shields/readthedocs]][docs/aioplus]

## Key Features

* As easy as built-ins - but asynchronous;
* Early returns never cause unawaited coroutine warnings;
* Nearly the same API as the Python 3.13 standard blocking API.

## Getting Started

### Installation

The library is available as [`aioplus`][pypi/homepage] on PyPI:

```shell
pip install aioplus
```

### Usage

#### *aall*

For more, see the [documentation][docs/aioplus/aall].

```python
import asyncio

from aioplus import aall, arange

async def main() -> None:
    """Run the program."""
    aiterable = (num > 0 async for num in arange(2304))
    flg = await aall(aiterable)

if __name__ == "__main__":
    asyncio.run(main())
```

#### *aany*

For more, see the [documentation][docs/aioplus/aany].

```python
import asyncio

from aioplus import aany, arange

async def main() -> None:
    """Run the program."""
    aiterable = (num % 2 == 0 async for num in arange(2304))
    flg = await aany(aiterable)

if __name__ == "__main__":
    asyncio.run(main())
```

#### *abatched*

For more, see the [documentation][docs/aioplus/abatched].

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

#### *acount*

For more, see the [documentation][docs/aioplus/acount].

```python
import asyncio

from aioplus import acount

async def main() -> None:
    """Run the program."""
    async for num in acount(start=23, step=4):
        print(num)

if __name__ == "__main__":
    asyncio.run(main())
```

#### *acycle*

For more, see the [documentation][docs/aioplus/acycle].

```python
import asyncio

from aioplus import acycle, arange

async def main() -> None:
    """Run the program."""
    async for num in acycle(arange(23)):
        print(num)

if __name__ == "__main__":
    asyncio.run(main())
```

#### *aenumerate*

For more, see the [documentation][docs/aioplus/aenumerate].

```python
import asyncio

from aioplus import aenumerate, arange

async def main() -> None:
    """Run the program."""
    async for index, num in aenumerate(arange(2304)):
        print(index, num)

if __name__ == "__main__":
    asyncio.run(main())
```

#### *aislice*

For more, see the [documentation][docs/aioplus/aislice].

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

For more, see the [documentation][docs/aioplus/alen].

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

#### *anth*

For more, see the [documentation][docs/aioplus/anth].

```python
import asyncio

from aioplus import anth, arange

async def main() -> None:
    """Run the program."""
    aiterable = arange(23)
    value = await anth(aiterable, n=4)
    print(f"value = {value}")

if __name__ == "__main__":
    asyncio.run(main())
```

#### *apairwise*

For more, see the [documentation][docs/aioplus/apairwise].

```python
import asyncio

from aioplus import apairwise, arange

async def main() -> None:
    """Run the program."""
    async for before, after in apairwise(arange(23)):
        print(f"{before} -> {after}")

if __name__ == "__main__":
    asyncio.run(main())
```

#### *arange*

For more, see the [documentation][docs/aioplus/arange].

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

#### *arepeat*

For more, see the [documentation][docs/aioplus/arepeat].

```python
import asyncio

from aioplus import arepeat

async def main() -> None:
    """Run the program."""
    async for num in arepeat(23, times=4):
        print(num)

if __name__ == "__main__":
    asyncio.run(main())
```

#### *areversed*

For more, see the [documentation][docs/aioplus/areversed].

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

For more, see the [documentation][docs/aioplus/awaitify].

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

## License

MIT License, Copyright (c) 2025 Sergei Y. Bogdanov. See [LICENSE][github/license] file.

<!-- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- -->

[docs/aioplus]: https://aioplus.readthedocs.io/
[docs/aioplus/aall]: https://aioplus.readthedocs.io/en/latest/aall.html
[docs/aioplus/aany]: https://aioplus.readthedocs.io/en/latest/aany.html
[docs/aioplus/abatched]: https://aioplus.readthedocs.io/en/latest/abatched.html
[docs/aioplus/acount]: https://aioplus.readthedocs.io/en/latest/acount.html
[docs/aioplus/acycle]: https://aioplus.readthedocs.io/en/latest/acycle.html
[docs/aioplus/aenumerate]: https://aioplus.readthedocs.io/en/latest/aenumerate.html
[docs/aioplus/aislice]: https://aioplus.readthedocs.io/en/latest/aislice.html
[docs/aioplus/alen]: https://aioplus.readthedocs.io/en/latest/alen.html
[docs/aioplus/anth]: https://aioplus.readthedocs.io/en/latest/anth.html
[docs/aioplus/apairwise]: https://aioplus.readthedocs.io/en/latest/apairwise.html
[docs/aioplus/arange]: https://aioplus.readthedocs.io/en/latest/arange.html
[docs/aioplus/arepeat]: https://aioplus.readthedocs.io/en/latest/arepeat.html
[docs/aioplus/areversed]: https://aioplus.readthedocs.io/en/latest/areversed.html
[docs/aioplus/awaitify]: https://aioplus.readthedocs.io/en/latest/awaitify.html

[github/license]: https://github.com/syubogdanov/aioplus/tree/main/LICENSE

[pypi/homepage]: https://pypi.org/project/aioplus/

[shields/pypi/downloads]: https://img.shields.io/pypi/dm/aioplus.svg?color=green
[shields/pypi/license]: https://img.shields.io/pypi/l/aioplus.svg?color=green
[shields/pypi/version]: https://img.shields.io/pypi/v/aioplus.svg?color=green
[shields/python/version]: https://img.shields.io/pypi/pyversions/aioplus.svg?color=green
[shields/readthedocs]: https://img.shields.io/readthedocs/aioplus?style=flat&color=green
