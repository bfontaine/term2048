# term2048

[![Build Status](https://img.shields.io/travis/bfontaine/term2048.svg)](https://travis-ci.org/bfontaine/term2048)

**term2048** is a terminal-based version of [2048][2048].

This is currently under development.

[2048]: http://gabrielecirulli.github.io/2048/

## Install

TODO

## Requirements

* Python 2.7
* Linux or OSX (the arrows key input function won’t work on Windows)

## Run

This will change in the future. For now:

```sh
git clone https://github.com/bfontaine/term2048.git
pip install -r term2048/requirements.txt
python term2048/src/term2048/ui.py
```

Then use arrow keys to move the board.

## Tests

    make check
