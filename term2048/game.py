# -*- coding: UTF-8 -*-
from __future__ import print_function

import atexit
import os
import os.path
import math
import sys

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
        keypress.SPACE:   Board.PAUSE,
    }

    __is_windows = os.name == 'nt'

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
    STORE_FILE = '%s/.term2048.store' % os.path.expanduser('~')

    def __init__(self, scores_file=SCORES_FILE, colors=COLORS,
                 store_file=STORE_FILE, clear_screen=True,
                 mode=None, azmode=False, **kws):
        """
        Create a new game.
            scores_file: file to use for the best score (default
                         is ~/.term2048.scores)
            colors: dictionnary with colors to use for each tile
            store_file: file that stores game session's snapshot
            mode: color mode. This adjust a few colors and can be 'dark' or
                  'light'. See the adjustColors functions for more info.
            other options are passed to the underlying Board object.
        """
        self.board = Board(**kws)
        self.score = 0
        self.scores_file = scores_file
        self.store_file = store_file
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
        try:
            with open(self.scores_file, 'r') as f:
                self.best_score = int(f.readline(), 10)
        except:
            self.best_score = 0
            return False
        return True

    def saveBestScore(self):
        """
        save current best score in the default file
        """
        if self.score > self.best_score:
            self.best_score = self.score
        try:
            with open(self.scores_file, 'w') as f:
                f.write(str(self.best_score))
        except:
            return False
        return True

    def incScore(self, pts):
        """
        update the current score by adding it the specified number of points
        """
        self.score += pts
        if self.score > self.best_score:
            self.best_score = self.score

    def readMove(self):
        """
        read and return a move to pass to a board
        """
        k = keypress.getKey()
        return Game.__dirs.get(k)

    def store(self):
        """
        save the current game session's score and data for further use
        """
        size = self.board.SIZE
        cells = []

        for i in range(size):
            for j in range(size):
                cells.append(str(self.board.getCell(j, i)))

        score_str = "%s\n%d" % (' '.join(cells), self.score)

        try:
            with open(self.store_file, 'w') as f:
                f.write(score_str)
        except:
            return False
        return True

    def restore(self):
        """
        restore the saved game score and data
        """

        size = self.board.SIZE

        try:
            with open(self.store_file, 'r') as f:
                lines = f.readlines()
                score_str = lines[0]
                self.score = int(lines[1])
        except:
            return False

        score_str_list = score_str.split(' ')
        count = 0

        for i in range(size):
            for j in range(size):
                value = score_str_list[count]
                self.board.setCell(j, i, int(value))
                count += 1

        return True

    def clearScreen(self):
        """Clear the console"""
        if self.clear_screen:
            os.system('cls' if self.__is_windows else 'clear')
        else:
            print('\n')

    def hideCursor(self):
        """
        Hide the cursor. Don't forget to call ``showCursor`` to restore
        the normal shell behavior. This is a no-op if ``clear_screen`` is
        falsy.
        """
        if not self.clear_screen:
            return
        if not self.__is_windows:
            sys.stdout.write('\033[?25l')

    def showCursor(self):
        """Show the cursor."""
        if not self.__is_windows:
            sys.stdout.write('\033[?25h')

    def loop(self):
        """
        main game loop. returns the final score.
        """
        pause_key = self.board.PAUSE
        margins = {'left': 4, 'top': 4, 'bottom': 4}

        atexit.register(self.showCursor)

        try:
            self.hideCursor()
            while True:
                self.clearScreen()
                print(self.__str__(margins=margins))
                if self.board.won() or not self.board.canMove():
                    break
                m = self.readMove()

                if (m == pause_key):
                    self.saveBestScore()
                    if self.store():
                        print("Game successfully saved. "
                              "Resume it with `term2048 --resume`.")
                        return self.score
                    print("An error ocurred while saving your game.")
                    return

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

        if c == 0:
            return '.' if self.__azmode else '  .'

        elif self.__azmode:
            az = {}
            for i in range(1, int(math.log(self.board.goal(), 2))):
                az[2 ** i] = chr(i + 96)

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
