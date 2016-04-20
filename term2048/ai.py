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

from __future__ import print_function   # import print() for printing to file

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

# Print results to file
def print_to_file(results):
    l = len(results)                                    # get number of results
    f = open('results.csv','w')                         # open file
    print("moves,largestTile,score", file=f)            # print title row
    for i in range(0, l):                               # loop over results
        print(str(results[i][0]) + \
        ',' + str(results[i][1]) + \
        ',' + str(results[i][2]), file=f)
    f.close()                                           # close file


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

startTime = time.time() # start the timer

results = run(random_ai,100000, size=4)

print('Highscore =    ' + str(max([res[1] for res in results] )))
print_to_file(results)  # print to file
endTime = time.time()   # end the timer
print('Elapsed time = ' + str(endTime - startTime))
