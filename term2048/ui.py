# -*- coding: UTF-8 -*-

from term2048.game import Game
import argparse

def start_game():
    """start a new game"""
    parser = argparse.ArgumentParser(description='2048 in your terminal')
    parser.add_argument('--mode', dest='mode',
            type=str, default=None, help='colors mode (dark or light)')
    args = parser.parse_args()

    Game(mode=args.mode).loop()
