========
term2048
========

.. image:: https://img.shields.io/travis/bfontaine/term2048.png
   :target: https://travis-ci.org/bfontaine/term2048
   :alt: Build status


.. image:: https://img.shields.io/coveralls/bfontaine/term2048.png
  :target: https://coveralls.io/r/bfontaine/term2048
  :alt: Coverage status

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

Then use arrow keys to move.

Requirements
------------

* Python 2.7
* Linux or OSX (the arrows key input function won’t work on Windows)

Tests
-----

Clone this repo, then: ::

    make check
