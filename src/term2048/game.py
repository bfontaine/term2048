# -*- coding: UTF-8 -*-

import os
import keypress
from board import Board
from colorama import init, Fore
init(autoreset=True)

class Game:
    __dirs = {
        keypress.UP:    Board.UP,
        keypress.DOWN:  Board.DOWN,
        keypress.LEFT:  Board.LEFT,
        keypress.RIGHT: Board.RIGHT
    }

    __clear = 'cls' if os.name == 'nt' else 'clear'

    def __init__(self):
        self.board = Board()
        self.score = 0

    def end(self):
        return not (self.board.won() or self.board.canMove())

    def readMove(self):
        k = keypress.getArrowKey()
        return Game.__dirs.get(k)

    def loop(self):
        while True:
            os.system(Game.__clear)
            print self
            self.score += self.board.move(self.readMove())
            if self.board.won() or not self.board.canMove():
                break

        print 'You won!' if self.board.won() else 'Game Over'

    def boardToString(self):
        b = self.board
        rg = xrange(Board.SIZE)
        s = "\n".join(
            [' '.join([b.getCellStr(x, y) for x in rg]) for y in rg])
        return s

    def __str__(self):
        b = self.boardToString()
        return b.replace('\n', ' \tScore: %5d\n' % self.score, 1)
