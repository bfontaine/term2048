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
        keypress.RIGHT: Board.RIGHT,
    }

    __clear = 'cls' if os.name == 'nt' else 'clear'

    __colors = {
           2: Fore.GREEN,
           4: Fore.BLUE,
           8: Fore.CYAN,
          16: Fore.RED,
          32: Fore.MAGENTA,
          64: Fore.CYAN,
         128: Fore.BLUE,
         256: Fore.MAGENTA,
         512: Fore.GREEN,
        1024: Fore.RED,
        2048: Fore.YELLOW,
    }

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
            print self.__str__(margins={'left':4, 'top':4, 'bottom':4})
            try:
                m = self.readMove()
            except KeyboardInterrupt:
                return
            self.score += self.board.move(m)
            if self.board.won() or not self.board.canMove():
                break

        print 'You won!' if self.board.won() else 'Game Over'

    def getCellStr(self, x, y):
        c = self.board.getCell(x, y)
        if c == 0:
            return '  .'

        if c == 1024:
            s = ' 1k'
        elif c == 2048:
            s = ' 2k'
        else:
            s = '%3d' % c
        return Game.__colors.get(c, Fore.RESET) + s + Fore.RESET

    def boardToString(self, margins={}):
        b = self.board
        rg = xrange(Board.SIZE)
        left = ' '*margins.get('left', 0)
        s = '\n'.join(
            [left + ' '.join([self.getCellStr(x, y) for x in rg]) for y in rg])
        return s

    def __str__(self, margins):
        b = self.boardToString(margins=margins)
        top = '\n'*margins.get('top', 0)
        bottom = '\n'*margins.get('bottom', 0)
        return top + b.replace('\n', ' \tScore: %5d\n' % self.score, 1) + bottom
