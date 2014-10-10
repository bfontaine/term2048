========
term2048
========

.. image:: https://img.shields.io/travis/bfontaine/term2048.png
   :target: https://travis-ci.org/bfontaine/term2048
   :alt: Build status

.. image:: https://img.shields.io/coveralls/bfontaine/term2048/master.png
   :target: https://coveralls.io/r/bfontaine/term2048?branch=master
   :alt: Coverage status

.. image:: https://img.shields.io/pypi/v/term2048.png
   :target: https://pypi.python.org/pypi/term2048
   :alt: Pypi package

.. image:: https://img.shields.io/pypi/dm/term2048.png
   :target: https://pypi.python.org/pypi/term2048

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

Play
----

.. code-block::

    term2048

Then use arrow keys to move. Since version 0.2.1 VI keys (h,j,k,l) are also
supported.

Use ``-h`` to check the list of available options, and ``--rules`` for the
game rules. Press ``<space>`` at any time during the game to pause the game
(since 0.2.5).

Tests
-----

Clone this repo, then: ::

    [sudo] make deps
    make check

Note: while ``term2048`` should work on Windows, tests are meant to run on
UNIX-like OSes and ``term2048.keypress``-related tests could fail if run on
Windows.

Contributions
-------------

* ``--version`` flag added by @aminb
* ``--rules`` flag added by @cardern
* Short ``-r`` and ``-v`` flags added by @yankuangshi
* Resume feature added by @pravj

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
