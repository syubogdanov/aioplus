aioplus
=======

|PyPI Version| |PyPI Downloads| |License| |Python Version| |Documentation|

Key Features
------------

-  As easy as built-ins - but asynchronous;
-  The same API as the Python 3.13 standard blocking API;
-  Early returns never cause unawaited coroutine warnings.

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

aall
----

For more, see the :doc:`aall <aall>`.

.. code-block:: python

    import asyncio

    from aioplus import aall, arange

    async def main() -> None:
        """Run the program."""
        aiterable = (num > 0 async for num in arange(2304))
        flg = await aall(aiterable)

    if __name__ == "__main__":
        asyncio.run(main())

aany
----

For more, see the :doc:`aany <aany>`.

.. code-block:: python

    import asyncio

    from aioplus import aany, arange

    async def main() -> None:
        """Run the program."""
        aiterable = (num % 2 == 0 async for num in arange(2304))
        flg = await aany(aiterable)

    if __name__ == "__main__":
        asyncio.run(main())

abatched
--------

For more, see the :doc:`abatched <abatched>`.

.. code-block:: python

    import asyncio

    from aioplus import abatched, arange

    async def main() -> None:
        """Run the program."""
        async for batch in abatched(arange(23), n=4):
            print(batch)

    if __name__ == "__main__":
        asyncio.run(main())

acount
------

For more, see the :doc:`acount <acount>`.

.. code-block:: python

    import asyncio

    from aioplus import acount

    async def main() -> None:
        """Run the program."""
        async for num in acount(start=23, step=4):
            print(num)

    if __name__ == "__main__":
        asyncio.run(main())

aenumerate
----------

For more, see the :doc:`aenumerate <aenumerate>`.

.. code-block:: python

    import asyncio

    from aioplus import aenumerate, arange

    async def main() -> None:
        """Run the program."""
        async for index, num in aenumerate(arange(2304)):
            print(index, num)

    if __name__ == "__main__":
        asyncio.run(main())

aislice
-------

For more, see the :doc:`aislice <aislice>`.

.. code-block:: python

    import asyncio

    from aioplus import aislice, arange

    async def main() -> None:
        """Run the program."""
        async for num in aislice(arange(23), 4):
            print(num)

    if __name__ == "__main__":
        asyncio.run(main())

alen
----

For more, see the :doc:`alen <alen>`.

.. code-block:: python

    import asyncio

    from aioplus import alen, arange

    async def main() -> None:
        """Run the program."""
        aiterable = arange(2304)
        length = await alen(aiterable)
        print(f"len(aiterable) == {length}")

    if __name__ == "__main__":
        asyncio.run(main())

arange
------

For more, see the :doc:`arange <arange>`.

.. code-block:: python

    import asyncio

    from aioplus import arange

    async def main() -> None:
        """Run the program."""
        async for num in arange(2304):
            print(num)

    if __name__ == "__main__":
        asyncio.run(main())

arepeat
-------

For more, see the :doc:`arepeat <arepeat>`.

.. code-block:: python

    import asyncio

    from aioplus import arepeat

    async def main() -> None:
        """Run the program."""
        async for num in arepeat(23, times=4):
            print(num)

    if __name__ == "__main__":
        asyncio.run(main())

areversed
---------

For more, see the :doc:`areversed <areversed>`.

.. code-block:: python

    import asyncio

    from aioplus import arange, areversed

    async def main() -> None:
        """Run the program."""
        async for num in areversed(arange(2304)):
            print(num)

    if __name__ == "__main__":
        asyncio.run(main())

awaitify
--------

For more, see the :doc:`awaitify <awaitify>`.

.. code-block:: python

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

.. toctree::
   :caption: API Reference
   :hidden:
   :maxdepth: 1

   aall
   aany
   abatched
   acount
   aenumerate
   aislice
   alen
   arange
   arepeat
   areversed
   awaitify

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
