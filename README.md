# aioplus

[![PyPI Version][shields/pypi/version]][pypi/homepage]
[![PyPI Downloads][shields/pypi/downloads]][pypi/homepage]
[![License][shields/pypi/license]][github/license]
[![Python Version][shields/python/version]][pypi/homepage]
[![Documentation][shields/readthedocs]][docs/aioplus]

## Key Features

* `builtins`, `itertools` and `more-itertools` - but asynchronous;
* Seamless *sync*-*async* bridging (`awaitify`, `anextify`, etc.);
* Early returns never cause unawaited coroutine warnings.

## Getting Started

### Installation

The library is available as [`aioplus`][pypi/homepage] on PyPI:

```shell
pip install aioplus
```

### Usage

#### *CallerThreadExecutor*

For more, see the [documentation][docs/aioplus/CallerThreadExecutor].

```python
>>> executor = CallerThreadExecutor()
>>> loop = asyncio.new_event_loop()
>>> loop.set_default_executor(executor)
```

#### *aall*

For more, see the [documentation][docs/aioplus/aall].

```python
>>> aiterable = arange(23)
>>> await aall(aiterable)
False
```

#### *aany*

For more, see the [documentation][docs/aioplus/aany].

```python
>>> aiterable = arange(23)
>>> await aany(aiterable)
True
```

#### *abatched*

For more, see the [documentation][docs/aioplus/abatched].

```python
>>> aiterable = arange(23)
>>> [batch async for batch in abatched(aiterable, n=3)]
[(0, 1, 2), (3, 4, 5), ..., (18, 19, 20), (21, 22)]
```

#### *acount*

For more, see the [documentation][docs/aioplus/acount].

```python
>>> [num async for num in acount(start=23, step=4)]
[23, 27, 31, 35, 39, 43, 47, ...]
```

#### *acycle*

For more, see the [documentation][docs/aioplus/acycle].

```python
>>> aiterable = arange(23)
>>> [num async for num in acycle(aiterable)]
[0, 1, ..., 22, 23, 0, 1, ..., 22, 23, ...]
```

#### *aenumerate*

For more, see the [documentation][docs/aioplus/aenumerate].

```python
>>> aiterable = arange(4, 23)
>>> [(index, num) async for index, num in aenumerate(aiterable)]
[(0, 4), (1, 5), (2, 6), (3, 7), ..., (17, 21), (18, 22)]
```

#### *afirst*

For more, see the [documentation][docs/aioplus/afirst].

```python
>>> aiterable = arange(23)
>>> await afirst(aiterable)
0
```

#### *ahead*

For more, see the [documentation][docs/aioplus/ahead].

```python
>>> aiterable = arange(23)
>>> [num async for num in ahead(aiterable, n=4)]
[0, 1, 2, 3]
```

#### *aislice*

For more, see the [documentation][docs/aioplus/aislice].

```python
>>> aiterable = arange(2003)
>>> [num async for num in aislice(aiterable, 4, 23)]
[4, 5, 6, 7, 8, ..., 20, 21, 22]
```

#### *alast*

For more, see the [documentation][docs/aioplus/alast].

```python
>>> aiterable = arange(23)
>>> await alast(aiterable)
22
```

#### *alen*

For more, see the [documentation][docs/aioplus/alen].

```python
>>> aiterable = arange(23)
>>> await alen(aiterable)
23
```

#### *amax*

For more, see the [documentation][docs/aioplus/amax].

```python
>>> aiterable = arange(23)
>>> await amax(aiterable)
22
```

#### *amin*

For more, see the [documentation][docs/aioplus/amin].

```python
>>> aiterable = arange(23)
>>> await amin(aiterable)
0
```

#### *aminmax*

For more, see the [documentation][docs/aioplus/aminmax].

```python
>>> aiterable = arange(23)
>>> await aminmax(aiterable)
(0, 22)
```

#### *anextify*

For more, see the [documentation][docs/aioplus/anextify].

```python
>>> iterable = [0, 1, 2, 3, 4, 5]
>>> aiterable = anextify(iterable)
>>> [num async for num in aiterable]
[0, 1, 2, 3, 4, 5]
```

#### *anth*

For more, see the [documentation][docs/aioplus/anth].

```python
>>> aiterable = arange(23)
>>> await anth(aiterable, n=4)
4
```

#### *apairwise*

For more, see the [documentation][docs/aioplus/apairwise].

```python
>>> aiterable = arange(23)
>>> [pair async for pair in apairwise(aiterable)]
[(0, 1), (1, 2), (2, 3), ..., (20, 21), (21, 22)]
```

#### *arange*

For more, see the [documentation][docs/aioplus/arange].

```python
>>> [num async for num in arange(23)]
[0, 1, 2, 3, 4, ..., 19, 20, 21, 22]
```

#### *arepeat*

For more, see the [documentation][docs/aioplus/arepeat].

```python
>>> [num async for num in arepeat(23, times=4)]
[23, 23, 23, 23]
```

#### *areversed*

For more, see the [documentation][docs/aioplus/areversed].

```python
>>> aiterable = arange(23)
>>> [num async for num in areversed(aiterable)]
[22, 21, 20, 19, 18, ..., 4, 3, 2, 1, 0]
```

#### *asum*

For more, see the [documentation][docs/aioplus/asum].

```python
>>> aiterable = arange(23)
>>> await asum(aiterable)
253
```

#### *atail*

For more, see the [documentation][docs/aioplus/atail].

```python
>>> aiterable = arange(23)
>>> [num async for num in atail(aiterable, n=4)]
[19, 20, 21, 22]
```

#### atriplewise

For more, see the [documentation][docs/aioplus/atriplewise].

```python
>>> aiterable = arange(23)
>>> [triplet async for triplet in atriplewise(aiterable)]
[(0, 1, 2), (1, 2, 3), ..., (19, 20, 21), (20, 21, 22)]
```

#### *awaitify*

For more, see the [documentation][docs/aioplus/awaitify].

```python
>>> aprint = awaitify(print)
>>> await aprint("4 -> 23")
4 -> 23
```

#### awindowed

For more, see the [documentation][docs/aioplus/awindowed].

```python
>>> aiterable = arange(23)
>>> [window async for window in awindowed(aiterable, n=3)]
[(0, 1, 2), (1, 2, 3), ..., (19, 20, 21), (20, 21, 22)]
```

## License

MIT License, Copyright (c) 2025 Sergei Y. Bogdanov. See [LICENSE][github/license] file.

<!-- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- -->

[docs/aioplus]: https://aioplus.readthedocs.io/
[docs/aioplus/CallerThreadExecutor]: https://aioplus.readthedocs.io/en/latest/CallerThreadExecutor.html
[docs/aioplus/aall]: https://aioplus.readthedocs.io/en/latest/aall.html
[docs/aioplus/aany]: https://aioplus.readthedocs.io/en/latest/aany.html
[docs/aioplus/abatched]: https://aioplus.readthedocs.io/en/latest/abatched.html
[docs/aioplus/acount]: https://aioplus.readthedocs.io/en/latest/acount.html
[docs/aioplus/acycle]: https://aioplus.readthedocs.io/en/latest/acycle.html
[docs/aioplus/aenumerate]: https://aioplus.readthedocs.io/en/latest/aenumerate.html
[docs/aioplus/afirst]: https://aioplus.readthedocs.io/en/latest/afirst.html
[docs/aioplus/ahead]: https://aioplus.readthedocs.io/en/latest/ahead.html
[docs/aioplus/aislice]: https://aioplus.readthedocs.io/en/latest/aislice.html
[docs/aioplus/alast]: https://aioplus.readthedocs.io/en/latest/alast.html
[docs/aioplus/alen]: https://aioplus.readthedocs.io/en/latest/alen.html
[docs/aioplus/amax]: https://aioplus.readthedocs.io/en/latest/amax.html
[docs/aioplus/amin]: https://aioplus.readthedocs.io/en/latest/amin.html
[docs/aioplus/aminmax]: https://aioplus.readthedocs.io/en/latest/aminmax.html
[docs/aioplus/anextify]: https://aioplus.readthedocs.io/en/latest/anextify.html
[docs/aioplus/anth]: https://aioplus.readthedocs.io/en/latest/anth.html
[docs/aioplus/apairwise]: https://aioplus.readthedocs.io/en/latest/apairwise.html
[docs/aioplus/arange]: https://aioplus.readthedocs.io/en/latest/arange.html
[docs/aioplus/arepeat]: https://aioplus.readthedocs.io/en/latest/arepeat.html
[docs/aioplus/areversed]: https://aioplus.readthedocs.io/en/latest/areversed.html
[docs/aioplus/asum]: https://aioplus.readthedocs.io/en/latest/asum.html
[docs/aioplus/atail]: https://aioplus.readthedocs.io/en/latest/atail.html
[docs/aioplus/atriplewise]: https://aioplus.readthedocs.io/en/latest/atriplewise.html
[docs/aioplus/awaitify]: https://aioplus.readthedocs.io/en/latest/awaitify.html
[docs/aioplus/awindowed]: https://aioplus.readthedocs.io/en/latest/awindowed.html

[github/license]: https://github.com/syubogdanov/aioplus/tree/main/LICENSE

[pypi/homepage]: https://pypi.org/project/aioplus/

[shields/pypi/downloads]: https://img.shields.io/pypi/dm/aioplus.svg?color=green
[shields/pypi/license]: https://img.shields.io/pypi/l/aioplus.svg?color=green
[shields/pypi/version]: https://img.shields.io/pypi/v/aioplus.svg?color=green
[shields/python/version]: https://img.shields.io/pypi/pyversions/aioplus.svg?color=green
[shields/readthedocs]: https://img.shields.io/readthedocs/aioplus?style=flat&color=green
