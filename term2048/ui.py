# -*- coding: UTF-8 -*-
from __future__ import print_function

from term2048.game import Game

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

def start_game():
    """start a new game"""
    if not __has_argparse:
        __print_argparse_warning()
        args = {'mode': None}
    else:
        parser = argparse.ArgumentParser(description='2048 in your terminal')
        parser.add_argument('--mode', dest='mode',
                type=str, default=None, help='colors mode (dark or light)')
        args = parser.parse_args()

    Game(mode=args.mode).loop()
