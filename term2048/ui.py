# -*- coding: UTF-8 -*-

from term2048.game import Game
import argparse

def start_game():
    """start a new game"""
    parser = argparse.ArgumentParser(description='2048 in your terminal')
    parser.add_argument('--mode', dest='mode',
            type=str, default=None, help='colors mode (dark or light)')
    parser.add_argument('--ak', dest='akmode',
            action='store_true', help='Use the letters a-k instead of 2-2048')
    args = parser.parse_args()

    Game(mode=args.mode, akmode=args.akmode).loop()
