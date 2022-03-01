# term2048 Changelog

## v1.0.0 (unreleased)

* Drop active support for Python 2.6, 3.2, 3.3 and 3.4. While the code may still work for these versions, we can’t test
  it because GitHub Actions doesn’t support them.
* Use Poetry as a build tool

### Code changes

These changes don’t affect you as a player; only if you’re using the Python module in your code.

#### Breaking changes

* Remove `board.Board.GOAL` and `board.Board.SIZE`; add `board.DEFAULT_GOAL` and `board.DEFAULT_SIZE` instead
* `Board#goal` and `Board#size` are now properties
* `Board#addTile` don’t accept a `value` anymore. To force a value, use `choices=(value,)`
* `Game.__dirs` is now named `Game.__directions`
* Remove `keypress.getArrowKey`. Use `keypress.getKey` instead

#### Other changes

* `ui.start_game` now accepts `args` for the parameters of the game
* Add some type hints

## v0.2.7 (2019-06-04)

* Fix encoding issues in `setup.py` on Windows

## v0.2.6 (2018-06-17)

* the cursor is now hidden on macOS/Linux (#31)
* fix disappearing tiles in PowerShell (#24)

## v0.2.5 (2014-10-11)

* pause and resume games (#30)
* Vim keys support for Windows (was only for Linux/OSX before)

## v0.2.4 (2014-07-07)

* argparse dependency added for all versions. It’s normally included in the
  stdlib for Python >2.6, but the code is cleaner if we don’t have
  2.6-specific pieces of code
* short flags for `--rules` (`-r`) and `--version` (`-v`) (#27)
* unused `game.end` function removed

## v0.2.3 (2014-03-24)

* `--rules` flag added (#25)

## v0.2.2 (2014-03-15)

* `--version` flag added (#18)
* colors issue fixed (#19)
* minor bug fixes

## v0.2.1 (2014-03-14)

* Indentation error in the game loop fixed

## v0.2.0 (2014-03-14)

* Python 2.6 and 3.x support
* Spawn probabilities fixed
* Colors improved
* Vim keys support
* Windows support
* AZ mode with letters instead of numbers in the UI
* A few bugs fixes and other minor improvements

## v0.1.7 (2014-03-14)

* `--mode` option added to change the colors mode

## v0.1.6 (2014-03-14)

* random collapse bug fixed

## v0.1.5 (2014-03-14)

* tiles don't spawn if nothing moved, like in the original game

## v0.1.4 (2014-03-14)

* best score support, bug fixes, minor UI improvements

## v0.1.3 (2014-03-14)

* using setuptools

## v0.1.2 (2014-03-14)

* better documentation, working executable

## v0.1.1 (2014-03-13)

* executable environment fix

## v0.1.0 (2014-03-13)

* Initial release
