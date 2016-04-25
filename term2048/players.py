# Create AI in this file, so we do not mess with ai.py

import random
from board import Board

def biasRandom_ai(board, score):
    r = random.random()
    if r < 0.6:
        return Board.UP
    elif r < 0.61:
        return Board.DOWN
    elif r < 0.90:
        return Board.LEFT
    else:
        return Board.RIGHT
