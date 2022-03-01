# -*- coding: UTF-8 -*-

"""
UI-related functions
"""

from __future__ import print_function

import sys
import argparse

try:
    import typing
except ImportError:
    pass  # Python 2.6 and 3.4

from term2048.game import Game


def print_version_and_exit():
    """print term2048's current version and exit"""
    from term2048 import __version__
    print("term2048 v%s" % __version__)
    sys.exit(0)


def print_rules_and_exit():
    """print 2048's rules and exit"""
    print("""Use your arrow keys to move the tiles.
When two tiles with the same value touch they merge into one with the sum of
their value! Try to reach 2048 to win.""")
    sys.exit(0)


def parse_cli_args():
    """parse args from the CLI and return a dict"""
    parser = argparse.ArgumentParser(description='2048 in your terminal')
    parser.add_argument('--mode', dest='mode', type=str,
                        default=None, help='colors mode (dark or light)')
    parser.add_argument('--az', dest='azmode', action='store_true',
                        help='Use the letters a-z instead of numbers')
    parser.add_argument('--resume', dest='resume', action='store_true',
                        help='restart the game from where you left')
    parser.add_argument('-v', '--version', action='store_true')
    parser.add_argument('-r', '--rules', action='store_true')
    return vars(parser.parse_args())


def start_game(
        debug=False,
        args=None,  # type: typing.Optional[typing.Dict[str, typing.Any]]
):
    """
    Start a new game.

    :param debug: if set to `True`, the game object is returned and the game loop isn't fired.
    :param args: if provided, the function uses them as arguments instead of parsing `sys.argv`.
    """
    if args is None:
        args = parse_cli_args()

    if args.get('version'):
        print_version_and_exit()

    if args.get('rules'):
        print_rules_and_exit()

    game = Game(**args)
    if args.get('resume'):
        game.restore()

    if debug:
        return game

    return game.loop()
