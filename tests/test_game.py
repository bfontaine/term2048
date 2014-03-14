# -*- coding: UTF-8 -*-
try:
    import unittest2 as unittest
except ImportError:
    import unittest

from colorama import Fore
from term2048.board import Board
from term2048.game import Game
from tempfile import NamedTemporaryFile
from os import remove

_BSIZE = Board.SIZE

class TestGame(unittest.TestCase):

    def setUp(self):
        Board.SIZE = _BSIZE
        Game.SCORES_FILE = None
        self.g = Game(scores_file=None)
        self.b = self.g.board

    def test_init_with_size_3_goal_4(self):
        g = Game(size=3, goal=4, scores_file=None)
        self.assertEqual(g.board.size(), 3)

    # == .end == #

    # == .saveBestScore == #

    def test_save_best_score_no_file(self):
        self.g.score = 42
        self.g.saveBestScore()
        self.assertEqual(self.g.best_score, 42)

    def test_save_best_score_with_file(self):
        scores_file = NamedTemporaryFile(delete=True)
        g = Game(scores_file=scores_file.name)
        g.best_score = 0
        g.score = 1000
        g.saveBestScore()
        self.assertEqual(g.best_score, 1000)

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

    # == .loadBestScore == #

    def test_init_with_local_scores_file(self):
        scores_file = NamedTemporaryFile(delete=False)
        scores_file.write('2048')
        scores_file.close()

        g = Game(scores_file=scores_file.name)
        self.assertEqual(g.best_score, 2048)

        remove(scores_file.name)

    def test_init_with_local_scores_file_fail(self):
        scores_file = NamedTemporaryFile(delete=False)
        scores_file.close()

        g = Game(scores_file=scores_file.name)

        remove(scores_file.name)

    # == .end == #
