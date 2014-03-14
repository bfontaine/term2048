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

Then use arrow keys to move. Use ``-h``  to check the list of available
options.

Tests
-----

Clone this repo, then: ::

    [sudo] pip2 install -r requirements.txt
    make check

If you’re using Python 2.6, you need to do this as well before running tests: ::

    [sudo] pip2 install -r py26-requirements.txt


Contributions
-------------

* Python 2.6 and 3.x support by @shaunduncan
* Tests instructions fixed by @olafleur
* Spawn probabilities fixed by @frankh
* Colors improved by @idosch
* hjkl keys support by @aminb
* Windows support by @valtron
* AZ mode by @JosephRedfern
* The first file-related tests were added by @taeram
