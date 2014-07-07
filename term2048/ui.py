# -*- coding: UTF-8 -*-
from __future__ import print_function

import sys
from term2048.game import Game

# set this to true when unit testing
debug = False

import argparse

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
    parser.add_argument('-v', '--version', action='store_true')
    parser.add_argument('-r', '--rules', action='store_true')
    return vars(parser.parse_args())


def start_game():
    """start a new game"""
    args = parse_cli_args()

    if args['version']:
        print_version_and_exit()

    if args['rules']:
        print_rules_and_exit()

    if not debug:
        Game(**args).loop()
