# -*- coding: UTF-8 -*-

import os
import os.path
import keypress
from board import Board
from colorama import init, Fore
init(autoreset=True)

class Game:
    """
    A 2048 game
    """

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

    SCORES_FILE = '%s/.term2048.scores' % os.path.expanduser('~')

    def __init__(self, scores_file=SCORES_FILE, **kws):
        self.board = Board(**kws)
        self.score = 0
        self.scores_file = scores_file
        self.loadBestScore()

    def loadBestScore(self):
        """
        load local best score from the default file
        """
        if self.scores_file is None or not os.path.exists(self.scores_file):
            self.best_score = 0
            return
        try:
            f = open(self.scores_file, 'r')
            self.best_score = int(f.readline(), 10)
            f.close()
        except:
            pass # fail silently

    def saveBestScore(self):
        """
        save current best score in the default file
        """
        if self.score > self.best_score:
            self.best_score = self.score
        try:
            f = open(self.scores_file, 'w')
            f.write(str(self.best_score))
            f.close()
        except:
            pass # fail silently

    def end(self):
        """
        return True if the game is finished
        """
        return not (self.board.won() or self.board.canMove())

    def readMove(self):
        """
        read and return a move to pass to a board
        """
        k = keypress.getArrowKey()
        return Game.__dirs.get(k)

    def loop(self):
        """
        main game loop
        """
        while True:
            os.system(Game.__clear)
            print self.__str__(margins={'left':4, 'top':4, 'bottom':4})
            if self.board.won() or not self.board.canMove():
                break
            try:
                m = self.readMove()
            except KeyboardInterrupt:
                self.saveBestScore()
                return
            self.score += self.board.move(m)
            if self.score > self.best_score:
                self.best_score = self.score

        self.saveBestScore()
        print 'You won!' if self.board.won() else 'Game Over'

    def getCellStr(self, x, y):
        """
        return a string representation of the cell located at x,y.
        """
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
        """
        return a string representation of the current board.
        """
        b = self.board
        rg = xrange(b.size())
        left = ' '*margins.get('left', 0)
        s = '\n'.join(
            [left + ' '.join([self.getCellStr(x, y) for x in rg]) for y in rg])
        return s

    def __str__(self, margins={}):
        b = self.boardToString(margins=margins)
        top = '\n'*margins.get('top', 0)
        bottom = '\n'*margins.get('bottom', 0)
        scores = ' \tScore: %5d  Best: %5d\n' % (self.score, self.best_score)
        return top + b.replace('\n', scores, 1) + bottom
