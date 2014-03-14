# -*- coding: UTF-8 -*-

import random

class Board():
    """
    A 2048 board
    """

    UP, DOWN, LEFT, RIGHT = 1, 2, 3, 4

    GOAL = 2048
    SIZE = 4

    def __init__(self, goal=GOAL, size=SIZE):
        self.__size = size
        self.__goal = goal
        self.__won = False
        self.cells = [[0]*self.__size for _ in xrange(self.__size)]
        self.addTile()
        self.addTile()

    def size(self):
        return self.__size

    def won(self):
        return self.__won

    def canMove(self):
        """
        test if a move is possible
        """
        if not self.filled():
            return True

        for y in xrange(0, self.__size):
            for x in xrange(0, self.__size):
                c = self.getCell(x, y)
                if (x < self.__size-1 and c == self.getCell(x+1, y)) \
                        or (y < self.__size-1 and c == self.getCell(x, y+1)):
                    return True

        return False

    def filled(self):
        return len(self.getEmptyCells()) == 0

    def addTile(self, value=None, choices=[2, 4]):
        """
        add a random tile in an empty cell
        """
        if value:
            choices = [value]

        v = random.choice(choices)
        empty = self.getEmptyCells()
        if empty:
            x, y = random.choice(empty)
            self.setCell(x, y, v)

    def getCell(self, x, y):
        return self.cells[y][x]

    def setCell(self, x, y, v):
        self.cells[y][x] = v

    def getLine(self, y):
        return [self.getCell(i, y) for i in xrange(0, self.__size)]

    def getCol(self, x):
        return [self.getCell(x, i) for i in xrange(0, self.__size)]

    def setLine(self, y, l):
        for i in xrange(0, self.__size):
            self.setCell(i, y, l[i])

    def setCol(self, x, l):
        for i in xrange(0, self.__size):
            self.setCell(x, i, l[i])

    def getEmptyCells(self):
        """
        return (x, y) for each cell
        """
        return [(x, y) for x in xrange(self.__size)
                           for y in xrange(self.__size) if self.getCell(x, y) == 0]

    def __collapseLineOrCol(self, line, d):
        """
        Merge tiles in a line or column according to a direction and return a
        tuple with the new line and the score for the move on this line
        """
        if (d == Board.LEFT or d == Board.UP):
            rg = xrange(0, self.__size-1)
        else:
            rg = xrange(self.__size-2, -1, -1)

        pts = 0
        for i in rg:
            if line[i] == 0:
                continue
            if line[i] == line[i+1]:
                v = line[i]*2
                if v == self.__goal:
                    self.__won = True

                line[i] = v
                line[i+1] = 0
                pts += v

        return (line, pts)

    def __moveLineOrCol(self, line, d):
        """
        Move a line or column to a given direction (d)
        """
        nl = [c for c in line if c != 0]
        if d == Board.UP or d == Board.LEFT:
            return nl + [0] * (self.__size - len(nl))
        return [0] * (self.__size - len(nl)) + nl

    def move(self, d, add_tile=True):
        """
        move and return the move score
        """
        if d == Board.LEFT or d == Board.RIGHT:
            chg, get = self.setLine, self.getLine
        elif d == Board.UP or d == Board.DOWN:
            chg, get = self.setCol, self.getCol
        else:
            return 0

        score = 0

        for i in xrange(0, self.__size):
            line = self.__moveLineOrCol(get(i), d)
            collapsed, pts = self.__collapseLineOrCol(line, d)
            chg(i, self.__moveLineOrCol(collapsed, d))
            score += pts

        if add_tile:
            self.addTile()

        return score
