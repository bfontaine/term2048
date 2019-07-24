========
term2048
========

.. image:: https://img.shields.io/travis/bfontaine/term2048.svg
   :target: https://travis-ci.org/bfontaine/term2048
   :alt: Build status

.. image:: https://img.shields.io/coveralls/bfontaine/term2048/master.svg
   :target: https://coveralls.io/r/bfontaine/term2048?branch=master
   :alt: Coverage status

.. image:: https://img.shields.io/pypi/v/term2048.svg
   :target: https://pypi.python.org/pypi/term2048
   :alt: Pypi package

**term2048** is a terminal-based version of 2048_.

.. _2048: http://gabrielecirulli.github.io/2048/

.. image:: https://github.com/bfontaine/term2048/raw/master/img/term2048.png

Install
-------

.. code-block::

    pip install term2048

To upgrade a previous installation, use:

.. code-block::

    pip install -U term2048

To install via `snap`_:

::

    sudo snap install term2048

.. _snap: https://www.snapcraft.io

Install from source
~~~~~~~~~~~~~~~~~~~

.. code-block::

    git clone https://github.com/bfontaine/term2048.git && cd term2048
    [sudo] python setup.py install

Play
----

.. code-block::

    term2048

Then use arrow keys to move. VI keys (h,j,k,l) are also supported.

Use ``-h`` to check the list of available options, and ``--rules`` for the
game rules. Press ``<space>`` at any time during the game to pause it. You can
resume it later using ``term2048 --resume``.

Tests
-----

Clone this repo, then: ::

    [sudo] make deps
    make check

Note: while ``term2048`` should work on Windows, tests are meant to run on
UNIX-like OSes and ``term2048.keypress``-related tests may fail on Windows.

Contributions
-------------

* ``--version`` flag added by @aminb
* ``--rules`` flag added by @cardern
* Short ``-r`` and ``-v`` flags added by @yankuangshi
* Resume feature added by @pravj
* Snap installation method added by @LaughingLove

v0.2.0
~~~~~~

* Python 2.6 and 3.x support by @shaunduncan
* Tests instructions fixed by @olafleur
* Spawn probabilities fixed by @frankh
* Colors improved by @idosch
* hjkl keys support by @aminb
* Windows support by @valtron
* AZ mode by @JosephRedfern
* The first file-related tests were added by @taeram
