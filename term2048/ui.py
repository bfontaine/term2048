# -*- coding: UTF-8 -*-

from game import Game

def start_game(**kws):
    """start a new game"""
    Game(**kws).loop()
