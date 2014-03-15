# -*- coding: UTF-8 -*-
try:
    import unittest2 as unittest
except ImportError:
    import unittest

import keypress_mock as kp
from colorama import Fore, Style
from term2048.board import Board
from term2048.game import Game

import sys
import os
from tempfile import NamedTemporaryFile
from os import remove
from helpers import DevNull

_BSIZE = Board.SIZE

class TestGame(unittest.TestCase):

    def setUp(self):
        Board.SIZE = _BSIZE
        Game.SCORES_FILE = None
        self.g = Game(scores_file=None)
        self.b = self.g.board
        # don't print anything on stdout
        self.stdout = sys.stdout
        sys.stdout = DevNull()
        # mock os.system
        self.system = os.system
        self.sys_cmd = None
        def fake_system(*cmd):
            self.sys_cmd = cmd

        os.system = fake_system

    def tearDown(self):
        sys.stdout = self.stdout
        os.system = self.system
        kp._setCtrlC(False)

    def test_init_with_size_3_goal_4(self):
        g = Game(size=3, goal=4, scores_file=None)
        self.assertEqual(g.board.size(), 3)

    # == .saveBestScore == #

    def test_save_best_score_no_file(self):
        s = 42
        self.g.score = s
        self.g.saveBestScore()
        self.assertEqual(self.g.best_score, s)

    def test_save_best_score_with_file(self):
        s = 1000
        scores_file = NamedTemporaryFile(delete=True)
        g = Game(scores_file=scores_file.name)
        g.best_score = 0
        g.score = s
        g.saveBestScore()
        self.assertEqual(g.best_score, s)

    # == .loadBestScore == #

    def test_init_with_local_scores_file(self):
        s = 4241
        scores_file = NamedTemporaryFile(delete=False)
        scores_file.write(str(s).encode())
        scores_file.close()

        g = Game(scores_file=scores_file.name)
        self.assertEqual(g.best_score, s)

        remove(scores_file.name)

    def test_init_with_local_scores_file_fail(self):
        scores_file = NamedTemporaryFile(delete=False)
        scores_file.close()

        g = Game(scores_file=scores_file.name)

        remove(scores_file.name)

    # == .incScore == #

    def test_inc_0_score(self):
        s = 3
        self.g.score = s
        self.g.best_score = s
        self.g.incScore(0)
        self.assertEqual(self.g.score, s)
        self.assertEqual(self.g.best_score, s)

    def test_inc_2_score(self):
        s = 3
        i = 2
        self.g.score = s
        self.g.best_score = s
        self.g.incScore(i)
        self.assertEqual(self.g.score, s+i)
        self.assertEqual(self.g.best_score, s+i)

    def test_inc_score_update_best_score(self):
        s = 3
        i = 2
        self.g.score = s
        self.g.best_score = 0
        self.g.incScore(i)
        self.assertEqual(self.g.score, s+i)
        self.assertEqual(self.g.best_score, s+i)

    def test_inc_score_dont_update_best_score_if_higher(self):
        s = 3
        bs = 80
        i = 2
        self.g.score = s
        self.g.best_score = bs
        self.g.incScore(i)
        self.assertEqual(self.g.score, s+i)
        self.assertEqual(self.g.best_score, bs)

    # == .end == #

    def test_end_can_play(self):
        self.assertFalse(self.g.end())

    # == .readMove == #

    def test_read_unknown_move(self):
        kp._setNextKey(-1)
        self.assertEqual(self.g.readMove(), None)

    def test_read_known_move(self):
        kp._setNextKey(kp.LEFT)
        self.assertEqual(self.g.readMove(), Board.LEFT)

    # == .loop == #

    def test_simple_win_loop(self):
        kp._setNextKey(kp.UP)
        g = Game(goal=4, size=2, clear_screen=False)
        g.board.cells = [
            [2, 0],
            [2, 0]
        ]
        g.loop()

    def test_simple_win_loop_clear(self):
        kp._setNextKey(kp.UP)
        g = Game(goal=4, size=2)
        g.board.cells = [
            [2, 0],
            [2, 0]
        ]
        self.assertEqual(g.loop(), 4)
        if os.name == 'nt':
            self.assertEqual(self.sys_cmd, ('cls',))
        else:
            self.assertEqual(self.sys_cmd, ('clear',))

    def test_loop_interrupt(self):
        kp._setCtrlC(True)
        g = Game(goal=4, size=2)
        self.assertEqual(g.loop(), None)

    # == .getCellStr == #

    def test_getCellStr_0(self):
        self.b.setCell(0, 0, 0)
        self.assertEqual(self.g.getCellStr(0, 0), '  .')

    def test_getCellStr_unknown_number(self):
        self.b.setCell(0, 0, 42)
        self.assertEqual(self.g.getCellStr(0, 0),
                '%s 42%s' % (Fore.RESET, Style.RESET_ALL))

    def test_getCellStr_0_azmode(self):
        g = Game(azmode=True)
        g.board.setCell(0, 0, 0)
        self.assertEqual(g.getCellStr(0, 0), '.')

    def test_getCellStr_2(self):
        g = Game()
        g.board.setCell(0, 0, 2)
        self.assertRegexpMatches(g.getCellStr(0, 0), r'  2\x1b\[0m$')

    def test_getCellStr_1k(self):
        g = Game()
        g.board.setCell(0, 0, 1024)
        self.assertRegexpMatches(g.getCellStr(0, 0), r' 1k\x1b\[0m$')

    def test_getCellStr_2k(self):
        g = Game()
        g.board.setCell(0, 0, 2048)
        self.assertRegexpMatches(g.getCellStr(0, 0), r' 2k\x1b\[0m$')

    def test_getCellStr_2_azmode(self):
        g = Game(azmode=True)
        g.board.setCell(0, 0, 2)
        self.assertRegexpMatches(g.getCellStr(0, 0), r'a\x1b\[0m$')

    def test_getCellStr_unknown_number_azmode(self):
        g = Game(azmode=True)
        g.board.setCell(0, 0, 42)
        self.assertEqual(g.getCellStr(0, 0), '?')

    # == .boardToString == #

    def test_boardToString_height_no_margins(self):
        s = self.g.boardToString()
        self.assertEqual(len(s.split("\n")), self.b.size())

    # == .__str__ == #

    def test_str_height_no_margins(self):
        s = str(self.g)
        self.assertEqual(len(s.split("\n")), self.b.size())
