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

