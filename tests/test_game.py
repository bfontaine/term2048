# -*- coding: UTF-8 -*-

from colorama import Fore
import unittest
from term2048.board import Board
from term2048.game import Game

_BSIZE = Board.SIZE

class TestGame(unittest.TestCase):

    def setUp(self):
        Board.SIZE = _BSIZE
        Game.SCORES_FILE = None
        self.g = Game()
        self.b = self.g.board

    def test_init_with_size_3_goal_4(self):
        g = Game(size=3, goal=4)
        self.assertEqual(g.board.size(), 3)

    # == .saveBestScore == #

    def test_save_best_score_no_file(self):
        g = Game()
        g.score = 42
        g.saveBestScore()
        self.assertEqual(g.best_score, 42)

    # == .end == #

    def test_end_can_play(self):
        self.assertFalse(self.g.end())

    # == .getCellStr == #

    def test_getCellStr_unknown_number(self):
        self.b.setCell(0, 0, 0)
        self.assertEqual(self.g.getCellStr(0, 0), '  .')

    def test_getCellStr_unknown_number(self):
        self.b.setCell(0, 0, 42)
        self.assertEqual(self.g.getCellStr(0, 0),
                '%s 42%s' % (Fore.RESET, Fore.RESET))

    # == .boardToString == #

    def test_boardToString_height_no_margins(self):
        s = self.g.boardToString()
        self.assertEqual(len(s.split("\n")), self.b.size())

    # == .__str__ == #

    def test_str_height_no_margins(self):
        s = str(self.g)
        self.assertEqual(len(s.split("\n")), self.b.size())
