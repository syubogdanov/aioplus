aioplus
=======

|PyPI Version| |PyPI Downloads| |License| |Python Version| |Documentation|

Key Features
------------

* ``builtins``, ``itertools`` and ``more-itertools`` — but asynchronous;
* Seamless *sync*-*async* bridging (``awaitify``, ``anextify``, etc.);
* Early returns never cause unawaited coroutine warnings.

Getting Started
---------------

Installation
~~~~~~~~~~~~

The library is available as
`aioplus <https://pypi.org/project/aioplus/>`__ on PyPI:

.. code:: shell

   pip install aioplus

Usage
~~~~~

CallerThreadExecutor
--------------------

For more, see the :doc:`documentation <CallerThreadExecutor>`.

.. code-block:: python

    >>> executor = CallerThreadExecutor()
    >>> loop = asyncio.new_event_loop()
    >>> loop.set_default_executor(executor)

aall
----

For more, see the :doc:`documentation <aall>`.

.. code-block:: python

    >>> aiterable = arange(23)
    >>> await aall(aiterable)
    False

aany
----

For more, see the :doc:`documentation <aany>`.

.. code-block:: python

    >>> aiterable = arange(23)
    >>> await aany(aiterable)
    True

abatched
--------

For more, see the :doc:`documentation <abatched>`.

.. code-block:: python

    >>> aiterable = arange(23)
    >>> [batch async for batch in abatched(aiterable, n=3)]
    [(0, 1, 2), (3, 4, 5), ..., (18, 19, 20), (21, 22)]

achain
--------

For more, see the :doc:`documentation <achain>`.

.. code-block:: python

    >>> nums1 = arange(0, 3)
    >>> nums2 = arange(3, 6)
    >>> [num async for num in achain(nums1, nums2)]
    [0, 1, 2, 3, 4, 5]

acount
------

For more, see the :doc:`documentation <acount>`.

.. code-block:: python

    >>> [num async for num in acount(start=23, step=4)]
    [23, 27, 31, 35, 39, 43, 47, ...]

acycle
------

For more, see the :doc:`documentation <acycle>`.

.. code-block:: python

    >>> aiterable = arange(23)
    >>> [num async for num in acycle(aiterable)]
    [0, 1, ..., 22, 23, 0, 1, ..., 22, 23, ...]

aempty
------

For more, see the :doc:`documentation <aempty>`.

.. code-block:: python

    >>> aiterable = arange(23)
    >>> await aempty(aiterable)
    False

aenumerate
----------

For more, see the :doc:`documentation <aenumerate>`.

.. code-block:: python

    >>> aiterable = arange(4, 23)
    >>> [(index, num) async for index, num in aenumerate(aiterable)]
    [(0, 4), (1, 5), (2, 6), (3, 7), ..., (17, 21), (18, 22)]

afirst
------

For more, see the :doc:`documentation <afirst>`.

.. code-block:: python

    >>> aiterable = arange(23)
    >>> await afirst(aiterable)
    0

ahead
-----

For more, see the :doc:`documentation <ahead>`.

.. code-block:: python

    >>> aiterable = arange(23)
    >>> [num async for num in ahead(aiterable, n=4)]
    [0, 1, 2, 3]

aislice
-------

For more, see the :doc:`documentation <aislice>`.

.. code-block:: python

    >>> aiterable = arange(2003)
    >>> [num async for num in aislice(aiterable, 4, 23)]
    [4, 5, 6, 7, 8, ..., 20, 21, 22]

alast
-----

For more, see the :doc:`documentation <alast>`.

.. code-block:: python

    >>> aiterable = arange(23)
    >>> await alast(aiterable)
    22

alen
----

For more, see the :doc:`documentation <alen>`.

.. code-block:: python

    >>> aiterable = arange(23)
    >>> await alen(aiterable)
    23

amax
----

For more, see the :doc:`documentation <amax>`.

.. code-block:: python

    >>> aiterable = arange(23)
    >>> await amax(aiterable)
    22

amin
----

For more, see the :doc:`documentation <amin>`.

.. code-block:: python

    >>> aiterable = arange(23)
    >>> await amin(aiterable)
    0

aminmax
-------

For more, see the :doc:`documentation <aminmax>`.

.. code-block:: python

    >>> aiterable = arange(23)
    >>> await aminmax(aiterable)
    (0, 22)

anextify
--------

For more, see the :doc:`documentation <anextify>`.

.. code-block:: python

    >>> iterable = [0, 1, 2, 3, 4, 5]
    >>> aiterable = anextify(iterable)
    >>> [num async for num in aiterable]
    [0, 1, 2, 3, 4, 5]

anth
----

For more, see the :doc:`documentation <anth>`.

.. code-block:: python

    >>> aiterable = arange(23)
    >>> await anth(aiterable, n=4)
    4

apairwise
---------

For more, see the :doc:`documentation <apairwise>`.

.. code-block:: python

    >>> aiterable = arange(23)
    >>> [pair async for pair in apairwise(aiterable)]
    [(0, 1), (1, 2), (2, 3), ..., (20, 21), (21, 22)]

apostpend
---------

For more, see the :doc:`documentation <apostpend>`.

.. code-block:: python

    >>> [num async for num in apostpend(arange(4), 4)]
    [0, 1, 2, 3, 4]

aprepend
---------

For more, see the :doc:`documentation <aprepend>`.

.. code-block:: python

    >>> [num async for num in aprepend(0, arange(1, 5))]
    [0, 1, 2, 3, 4]

arace
-----

For more, see the :doc:`documentation <arace>`.

.. code-block:: python

    >>> nums1 = arange(0, 3)
    >>> nums2 = arange(3, 6)
    >>> nums3 = arange(6, 9)
    >>> [num async for num in arace(nums1, nums2, nums3)]
    [0, 6, 3, 1, 4, 7, 5, 2, 8]

arange
------

For more, see the :doc:`documentation <arange>`.

.. code-block:: python

    >>> [num async for num in arange(23)]
    [0, 1, 2, 3, 4, ..., 19, 20, 21, 22]

arepeat
-------

For more, see the :doc:`documentation <arepeat>`.

.. code-block:: python

    >>> [num async for num in arepeat(23, times=4)]
    [23, 23, 23, 23]

areversed
---------

For more, see the :doc:`documentation <areversed>`.

.. code-block:: python

    >>> aiterable = arange(23)
    >>> [num async for num in areversed(aiterable)]
    [22, 21, 20, 19, 18, ..., 4, 3, 2, 1, 0]

asum
----

For more, see the :doc:`documentation <asum>`.

.. code-block:: python

    >>> aiterable = arange(23)
    >>> await asum(aiterable)
    253

atabulate
---------

For more, see the :doc:`documentation <atabulate>`.

.. code-block:: python

    >>> afunc = awaitify(lambda x: x * x)
    >>> [num async for num in atabulate(afunc)]
    [0, 1, 4, 9, 16, 25, 36, 49, ...]

atail
-----

For more, see the :doc:`documentation <atail>`.

.. code-block:: python

    >>> aiterable = arange(23)
    >>> [num async for num in atail(aiterable, n=4)]
    [19, 20, 21, 22]

atriplewise
-----------

For more, see the :doc:`documentation <atriplewise>`.

.. code-block:: python

    >>> aiterable = arange(23)
    >>> [triplet async for triplet in atriplewise(aiterable)]
    [(0, 1, 2), (1, 2, 3), ..., (19, 20, 21), (20, 21, 22)]

awaitify
--------

For more, see the :doc:`documentation <awaitify>`.

.. code-block:: python

    >>> aprint = awaitify(print)
    >>> await aprint("4 -> 23")
    4 -> 23

awindowed
---------

For more, see the :doc:`documentation <awindowed>`.

.. code-block:: python

    >>> aiterable = arange(23)
    >>> [window async for window in awindowed(aiterable, n=3)]
    [(0, 1, 2), (1, 2, 3), ..., (19, 20, 21), (20, 21, 22)]

azip
----

For more, see the :doc:`documentation <azip>`.

.. code-block:: python

    >>> xs = arange(42)
    >>> ys = arange(4, 23)
    >>> [(x, y) async for x, y in azip(xs, ys)]
    [(0, 4), (1, 5), (2, 6), ..., (18, 22)]

.. toctree::
    :caption: API Reference
    :hidden:
    :maxdepth: 1

    CallerThreadExecutor
    aall
    aany
    abatched
    achain
    acount
    acycle
    aempty
    aenumerate
    afirst
    ahead
    aislice
    alast
    alen
    amax
    amin
    aminmax
    anextify
    anth
    apairwise
    apostpend
    aprepend
    arace
    arange
    arepeat
    areversed
    asum
    atail
    atabulate
    atriplewise
    awaitify
    awindowed
    azip

License
-------

MIT License, Copyright (c) 2025 Sergei Y. Bogdanov. See
`LICENSE <https://github.com/syubogdanov/aioplus/tree/main/LICENSE>`__ file.

.. |PyPI Version| image:: https://img.shields.io/pypi/v/aioplus.svg?color=green
   :target: https://pypi.org/project/aioplus/
.. |PyPI Downloads| image:: https://img.shields.io/pypi/dm/aioplus.svg?color=green
   :target: https://pypi.org/project/aioplus/
.. |License| image:: https://img.shields.io/pypi/l/aioplus.svg?color=green
   :target: https://github.com/syubogdanov/aioplus/tree/main/LICENSE
.. |Python Version| image:: https://img.shields.io/pypi/pyversions/aioplus.svg?color=green
   :target: https://pypi.org/project/aioplus/
.. |Documentation| image:: https://img.shields.io/readthedocs/aioplus?style=flat&color=green
   :target: https://aioplus.readthedocs.io/
