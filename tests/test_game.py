# -*- coding: UTF-8 -*-

import unittest
from term2048.board import Board
from term2048.game import Game

_BSIZE = Board.SIZE

class TestGame(unittest.TestCase):

    def setUp(self):
        Board.SIZE = _BSIZE
        self.g = Game()
        self.b = self.g.board


    # == .getCell == #
    def test_getCellStr_empty(self):
        x, y = 3, 1
        self.b.cells[y][x] = 0
        self.assertEqual(self.g.getCellStr(x, y), '   .')

    def test_getCellStr_2(self):
        x, y = 3, 1
        self.b.cells[y][x] = 2
        self.assertEqual(self.g.getCellStr(x, y), '   2')

    def test_getCellStr_2048(self):
        x, y = 3, 1
        self.b.cells[y][x] = 2048
        self.assertEqual(self.g.getCellStr(x, y), '2048')
