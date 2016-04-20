# Idea here is that to make a new AI-impelmentation you should write a
# function that takes as input board-object and current score (number).
#
# Your function should return value form list [Board.UP, Board.LEFT, ..]
# according to which move your AI decies to make. As respond to that move
# it receives updated board and score.
#
# To play one game with your AI, use run()-function or run_gui().
# Both take your function as first input and additional parameters
# defined in Board and Game classes.
#
# For example run(your_function, size=8) would set board size to 8.

import random
import time

from game import Game
from board import Board

def get_state(board):
    """
    Append all rows to one array, starting from the uppermost one.
    """
    s = range(board.size())
    return [ board.getCell(x,y) for y in s for x in s]

def largest_tile(board):
    """ Returns the value of the largest tile at board """
    return max(get_state(board))

def random_ai(board, score):
    moves = [Board.UP, Board.DOWN, Board.LEFT, Board.RIGHT]
    r = random.randint(0,3)
    #time.sleep(0.2)
    return moves[r]

# Use this to run your AI with GUI
def run_gui(ai_function, **kws):
    game = Game(**kws)
    game.ai_loop(ai_function)
    
def run(ai_function, times=1,  **kws):
    results = []
    while(times > 0):
        score = 0
        moves = 0
        board = Board(**kws)
        while True:
            if board.won() or not board.canMove():
                break
            move = ai_function(board,score)
            score += board.move(move)
            moves += 1
    
        results.append((moves, largest_tile(board), score))
        times -= 1

    return results
    
results = run(random_ai,10000)
print( max([res[1] for res in results] ))
