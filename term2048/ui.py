# -*- coding: UTF-8 -*-
from __future__ import print_function

import sys
from term2048.game import Game

# set this to true when unit testing
debug = False

__has_argparse = True
try:
    import argparse
except ImportError:
    __has_argparse = False


def __print_argparse_warning():
    """print a warning for Python 2.6 users who don't have argparse"""
    print("""WARNING:
        You seems to be running Python 2.6 without 'argparse'. Please install
        the module so I can handle your options:
            [sudo] pip install argparse
        I'll continue without processing any option.""")


def print_version_and_exit():
    from term2048 import __version__
    print("term2048 v%s" % __version__)
    sys.exit(0)


def print_rules_and_exit():
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
    parser.add_argument('--version', action='store_true')
    parser.add_argument('--rules', action='store_true')
    return vars(parser.parse_args())


def start_game():
    """start a new game"""
    if not __has_argparse:
        __print_argparse_warning()
        args = {}
    else:
        args = parse_cli_args()

        if args['version']:
            print_version_and_exit()

        if args['rules']:
            print_rules_and_exit()

    if not debug:
        Game(**args).loop()
