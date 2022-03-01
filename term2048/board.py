# -*- coding: UTF-8 -*-

"""
Board-related things.
"""

import random

try:
    import typing
except ImportError:
    pass  # Python 2.6 and 3.4

DEFAULT_GOAL = 2048
DEFAULT_SIZE = 4


class Board(object):
    """
    A 2048 board.
    """

    UP, DOWN, LEFT, RIGHT, PAUSE = 1, 2, 3, 4, 5

    def __init__(self, goal=DEFAULT_GOAL, size=DEFAULT_SIZE, **_kwargs):
        self.__size = size
        self.__size_range = list(range(0, self.__size))
        self.__goal = goal
        self.__won = False
        self.cells = [[0] * self.__size for _ in range(self.__size)]
        self.addTile()
        self.addTile()

    @property
    def size(self):
        """return the board size"""
        return self.__size

    @property
    def goal(self):
        """return the board goal"""
        return self.__goal

    def won(self):
        """
        return True if the board contains at least one tile with the board goal
        """
        return self.__won

    def canMove(self):
        """
        test if a move is possible
        """
        if not self.filled():
            return True

        for y in self.__size_range:
            for x in self.__size_range:
                c = self.getCell(x, y)
                if (x < self.__size - 1 and c == self.getCell(x + 1, y)) \
                        or (y < self.__size - 1 and c == self.getCell(x, y + 1)):
                    return True

        return False

    def filled(self):
        """
        return true if the game is totally filled.
        """
        for x in self.__size_range:
            for y in self.__size_range:
                if self.getCell(x, y) == 0:
                    return False

        return True

    def addTile(self, choices=(2, 2, 2, 2, 2, 2, 2, 2, 2, 4)):  # type: (typing.Tuple[int, ...]) -> None
        """
        Add a random tile in an empty cell, if possible.

        :param choices: a list of possible choices for the value of the tile.
        """
        v = random.choice(choices)
        empty = self.getEmptyCells()
        if empty:
            x, y = random.choice(empty)
            self.setCell(x, y, v)

    def getCell(self, x, y):  # type: (int, int) -> int
        """return the cell value at x,y"""
        return self.cells[y][x]

    def setCell(self, x, y, value):  # type: (int, int, typing.Any) -> None
        """set the cell value at x,y"""
        self.cells[y][x] = value

    def getLine(self, y):  # type: (int) -> typing.List[int]
        """return the y-th line, starting at 0"""
        return self.cells[y]

    def getCol(self, x):  # type: (int) -> typing.List[int]
        """return the x-th column, starting at 0"""
        return [self.getCell(x, i) for i in self.__size_range]

    def setLine(self, y, line):  # type: (int, typing.List[int]) -> None
        """set the y-th line, starting at 0"""
        self.cells[y] = line[:]

    def setCol(self, x, line):  # type: (int, typing.List[int]) -> None
        """set the x-th column, starting at 0"""
        for i in range(0, self.__size):
            self.setCell(x, i, line[i])

    def getEmptyCells(self):  # type: () -> typing.List[typing.Tuple[int, int]]
        """return a (x, y) pair for each empty cell"""
        return [(x, y)
                for x in self.__size_range
                for y in self.__size_range if self.getCell(x, y) == 0]

    def __collapseLineOrCol(self, line, direction):
        # type: (typing.List[int], int) -> typing.Tuple[typing.Any, int]
        """
        Merge tiles in a line or column according to a direction and return a
        tuple with the new line and the score for the move on this line
        """
        if direction == Board.LEFT or direction == Board.UP:
            inc = 1
            rg = range(0, self.__size - 1, inc)
        else:
            inc = -1
            rg = range(self.__size - 1, 0, inc)

        move_score = 0
        for i in rg:
            if line[i] == 0:
                continue
            if line[i] == line[i + inc]:
                new_cell_value = line[i] * 2
                if new_cell_value == self.__goal:
                    self.__won = True

                line[i] = new_cell_value
                line[i + inc] = 0
                move_score += new_cell_value

        return line, move_score

    def __moveLineOrCol(self, line, direction):  # type: (typing.Any, int) -> typing.List[int]
        """
        Move a line or column to a given direction.
        """
        filled_cells = [cell for cell in line if cell != 0]
        if direction == Board.UP or direction == Board.LEFT:
            return filled_cells + [0] * (self.__size - len(filled_cells))
        return [0] * (self.__size - len(filled_cells)) + filled_cells

    def move(self, direction, add_tile=True):  # type: (int, bool) -> int
        """
        move and return the move score
        """

        if direction == Board.LEFT or direction == Board.RIGHT:
            chg = self.setLine  # type: typing.Callable[[int, typing.List[int]], None]
            get = self.getLine  # type: typing.Callable[[int], typing.List[int]]
        elif direction == Board.UP or direction == Board.DOWN:
            chg = self.setCol
            get = self.getCol
        else:
            return 0

        moved = False
        score = 0

        for i in self.__size_range:
            # save the original line/col
            origin = get(i)
            # move it
            line = self.__moveLineOrCol(origin, direction)
            # merge adjacent tiles
            collapsed, pts = self.__collapseLineOrCol(line, direction)
            # move it again (for when tiles are merged, because empty cells are
            # inserted in the middle of the line/col)
            new = self.__moveLineOrCol(collapsed, direction)
            # set it back in the board
            chg(i, new)
            # did it change?
            if origin != new:
                moved = True
            score += pts

        # add a new tile only if something changed
        if moved and add_tile:
            self.addTile()

        return score
