# -*- coding: UTF-8 -*-
from __future__ import print_function

import os
import os.path
import math

from colorama import init, Fore, Style
init(autoreset=True)

from term2048 import keypress
from term2048.board import Board


class Game(object):
    """
    A 2048 game
    """

    __dirs = {
        keypress.UP:      Board.UP,
        keypress.DOWN:    Board.DOWN,
        keypress.LEFT:    Board.LEFT,
        keypress.RIGHT:   Board.RIGHT,
    }

    __clear = 'cls' if os.name == 'nt' else 'clear'

    COLORS = {
        2:    Fore.GREEN,
        4:    Fore.BLUE + Style.BRIGHT,
        8:    Fore.CYAN,
        16:   Fore.RED,
        32:   Fore.MAGENTA,
        64:   Fore.CYAN,
        128:  Fore.BLUE + Style.BRIGHT,
        256:  Fore.MAGENTA,
        512:  Fore.GREEN,
        1024: Fore.RED,
        2048: Fore.YELLOW,
        # just in case people set an higher goal they still have colors
        4096: Fore.RED,
        8192: Fore.CYAN,
    }

    # see Game#adjustColors
    # these are color replacements for various modes
    __color_modes = {
        'dark': {
            Fore.BLUE: Fore.WHITE,
            Fore.BLUE + Style.BRIGHT: Fore.WHITE,
        },
        'light': {
            Fore.YELLOW: Fore.BLACK,
        },
    }

    SCORES_FILE = '%s/.term2048.scores' % os.path.expanduser('~')

    def __init__(self, scores_file=SCORES_FILE, colors=COLORS,
                 clear_screen=True,
                 mode=None, azmode=False, **kws):
        """
        Create a new game.
            scores_file: file to use for the best score (default
                         is ~/.term2048.scores)
            colors: dictionnary with colors to use for each tile
            mode: color mode. This adjust a few colors and can be 'dark' or
                  'light'. See the adjustColors functions for more info.
            other options are passed to the underlying Board object.
        """
        self.board = Board(**kws)
        self.score = 0
        self.scores_file = scores_file
        self.clear_screen = clear_screen

        self.__colors = colors
        self.__azmode = azmode

        self.loadBestScore()
        self.adjustColors(mode)

    def adjustColors(self, mode='dark'):
        """
        Change a few colors depending on the mode to use. The default mode
        doesn't assume anything and avoid using white & black colors. The dark
        mode use white and avoid dark blue while the light mode use black and
        avoid yellow, to give a few examples.
        """
        rp = Game.__color_modes.get(mode, {})
        for k, color in self.__colors.items():
            self.__colors[k] = rp.get(color, color)

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
            pass  # fail silently

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
            pass  # fail silently

    def incScore(self, pts):
        """
        update the current score by adding it the specified number of points
        """
        self.score += pts
        if self.score > self.best_score:
            self.best_score = self.score

    def end(self):
        """
        return True if the game is finished
        """
        return not (self.board.won() or self.board.canMove())

    def readMove(self):
        """
        read and return a move to pass to a board
        """
        k = keypress.getKey()
        return Game.__dirs.get(k)

    def loop(self):
        """
        main game loop. returns the final score.
        """
        try:
            while True:
                if self.clear_screen:
                    os.system(Game.__clear)
                else:
                    print("\n")
                print(self.__str__(margins={'left': 4, 'top': 4, 'bottom': 4}))
                if self.board.won() or not self.board.canMove():
                    break
                m = self.readMove()
                self.incScore(self.board.move(m))

        except KeyboardInterrupt:
            self.saveBestScore()
            return

        self.saveBestScore()
        print('You won!' if self.board.won() else 'Game Over')
        return self.score

    def getCellStr(self, x, y):  # TODO: refactor regarding issue #11
        """
        return a string representation of the cell located at x,y.
        """
        c = self.board.getCell(x, y)

        az = {}
        for i in range(1, int(math.log(self.board.goal(), 2))):
            az[2 ** i] = chr(i + 96)

        if c == 0 and self.__azmode:
            return '.'
        elif c == 0:
            return '  .'

        elif self.__azmode:
            if c not in az:
                return '?'
            s = az[c]
        elif c == 1024:
            s = ' 1k'
        elif c == 2048:
            s = ' 2k'
        else:
            s = '%3d' % c

        return self.__colors.get(c, Fore.RESET) + s + Style.RESET_ALL

    def boardToString(self, margins={}):
        """
        return a string representation of the current board.
        """
        b = self.board
        rg = range(b.size())
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
