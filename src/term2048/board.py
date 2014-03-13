# -*- coding: UTF-8 -*-

import random

class Board():
    """
    A 2048 board
    """

    # FIXME:
    # * [ 2 2 2 ] -> right gives [ 0 4 2 ] instead of [ 0 2 4 ]
    # * [ 2 0 2 ] -> right gives [ 0 2 2 ] instead of [ 0 0 4 ]

    UP, DOWN, LEFT, RIGHT = 1, 2, 3, 4

    GOAL = 2048
    SIZE = 4

    def __init__(self):
        self.cells = [[0]*Board.SIZE for i in xrange(Board.SIZE)]
        self.addTile(2)
        self.addTile(2)
        self.__won = False

    def won(self):
        return self.__won

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

    def getCellStr(self, x, y):
        c = self.getCell(x, y)
        if c == 0:
            return '   .'
        return '%4d' % c

    def setCell(self, x, y, v):
        self.cells[y][x] = v

    def getLine(self, y):
        return [self.getCell(i, y) for i in xrange(0, Board.SIZE)]

    def getCol(self, x):
        return [self.getCell(x, i) for i in xrange(0, Board.SIZE)]

    def setLine(self, y, l):
        for i in xrange(0, Board.SIZE):
            self.setCell(i, y, l[i])

    def setCol(self, x, l):
        for i in xrange(0, Board.SIZE):
            self.setCell(x, i, l[i])

    def getEmptyCells(self):
        """
        return [x, y] for each cell
        """
        return [[x, y] for x in xrange(Board.SIZE)
                           for y in xrange(Board.SIZE) if self.getCell(x, y) == 0]

    def __collapseLineOrCol(self, line):
        """
        Merge tiles in a line or column
        """
        for i in xrange(0, Board.SIZE-1):
            if line[i] == line[i+1]:
                line[i] = 2*line[i]
                line[i+1] = 0
                if line[i] == Board.GOAL:
                    self.won = True

        return line

    def __moveLineOrCol(self, line, d):
        """
        Move a line or column to a given direction (d)
        """
        nl = [c for c in line if c != 0]
        if d == Board.UP or d == Board.LEFT:
            return nl + [0] * (Board.SIZE - len(nl))
        return [0] * (Board.SIZE - len(nl)) + nl

    def move(self, d):
        hz = (d == Board.LEFT or d == Board.RIGHT)
        chg, get = (self.setLine, self.getLine) if hz \
                        else (self.setCol, self.getCol)
        for i in xrange(0, Board.SIZE):
            chg(i, self.__moveLineOrCol(self.__collapseLineOrCol(get(i)), d))

        self.addTile()

    def __str__(self):
        s = "\n".join([' '.join(
                    [self.getCellStr(x, y) for x in xrange(Board.SIZE)])
                        for y in xrange(Board.SIZE)])
        return s
