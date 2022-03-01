# term2048

[![Pypi package](https://img.shields.io/pypi/v/term2048.svg)](https://pypi.python.org/pypi/term2048)

**term2048** is a terminal-based version of [2048](https://play2048.co/).

![](https://github.com/bfontaine/term2048/raw/master/img/term2048.png)

## Install

    pip install term2048

To upgrade a previous installation, use:

    pip install -U term2048

To install via [`snap`](https://www.snapcraft.io):

    sudo snap install term2048

### Install from source

    git clone https://github.com/bfontaine/term2048.git && cd term2048
    [sudo] python setup.py install

## Play

    term2048

Then use arrow keys to move. VI keys (<kbd>h</kbd>,<kbd>j</kbd>,<kbd>k</kbd>,<kbd>l</kbd>) are also
supported.

Use `-h` to check the list of available options, and `--rules` for the
game rules. Press the <kbd>space</kbd> key at any time during the game to pause it. You can
resume it later using `term2048 --resume`.

## Tests

Clone this repo, then:

    [sudo] make deps
    make check

Note: while `term2048` should work on Windows, tests are meant to run on
UNIX-like OSes and `term2048.keypress`-related tests may fail on Windows.

## Contributions
-------------

* `--version` flag added by @aminb
* `--rules` flag added by @cardern
* Short `-r` and `-v` flags added by @yankuangshi
* Resume feature added by @pravj
* Snap installation method added by @LaughingLove

### v0.2.0

* Python 2.6 and 3.x support by @shaunduncan
* Tests instructions fixed by @olafleur
* Spawn probabilities fixed by @frankh
* Colors improved by @idosch
* hjkl keys support by @aminb
* Windows support by @valtron
* AZ mode by @JosephRedfern
* The first file-related tests were added by @taeram
