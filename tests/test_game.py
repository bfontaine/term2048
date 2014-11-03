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
from os import remove
from tempfile import NamedTemporaryFile
from uuid import uuid4

from helpers import DevNull

_BSIZE = Board.SIZE

class TestGame(unittest.TestCase):

    def setUp(self):
        Board.SIZE = _BSIZE
        Game.SCORES_FILE = None
        self.g = Game(scores_file=None, store_file=None)
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

    def setWindows(self, game, isWin=True):
        setattr(game, '_Game__is_windows', isWin)

    def assertFileIsNotEmpty(self, path):
        with open(path, 'r') as f:
            f.seek(0, 2)
            size = f.tell()
        self.assertNotEqual(0, size)

    # == .init == #

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
        self.assertEqual(g.best_score, 0)

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

    # == .store/.restore == #

    def test_store_non_empty_file(self):
        store = NamedTemporaryFile(delete=False)
        store.close()
        g = Game(scores_file=None, store_file=store.name)
        self.assertTrue(g.store())
        self.assertFileIsNotEmpty(store.name)
        remove(store.name)

    def test_store_fail_return_false(self):
        store = NamedTemporaryFile(delete=False)
        store.close()
        os.chmod(store.name, 0)  # no rights at all
        g = Game(scores_file=None, store_file=store.name)
        self.assertFalse(g.store())
        os.chmod(store.name, 0o200)  # give me writing rights back
        remove(store.name)

    def test_store_restore_empty_game(self):
        store = NamedTemporaryFile(delete=False)
        store.close()
        g1 = Game(scores_file=None, store_file=store.name)
        self.assertTrue(g1.store())
        g2 = Game(scores_file=None, store_file=store.name)
        g2.board.setCell(0, 0, 16)
        self.assertTrue(g2.restore())
        self.assertIn(g2.board.getCell(0, 0), [0, 2, 4])
        remove(store.name)

    def test_restore_fail_return_false(self):
        store_name = '/i/dont/%s/exist/%s' % (uuid4(), uuid4())
        g = Game(scores_file=None, store_file=store_name)
        self.assertFalse(g.restore())

    # == .readMove == #

    def test_read_unknown_move(self):
        kp._setNextKey(-1)
        self.assertEqual(self.g.readMove(), None)

    def test_read_known_move(self):
        kp._setNextKey(kp.LEFT)
        self.assertEqual(self.g.readMove(), Board.LEFT)

    # == .clear == #

    def test_clear_with_no_clear_screen(self):
        g = Game(scores_file=None, store_file=None, clear_screen=False)
        g.clearScreen()
        self.assertEqual(sys.stdout.read(), '\n\n')  # \n + print's \n

    # == .hideCursor == #

    def test_hide_cursor_linux(self):
        g = Game(scores_file=None, store_file=None, clear_screen=True)
        self.setWindows(g, False)
        g.hideCursor()
        self.assertEqual(sys.stdout.read(), '\033[?25l')
        g.showCursor()

    def test_hide_cursor_windows(self):
        g = Game(scores_file=None, store_file=None, clear_screen=True)
        self.setWindows(g)
        g.hideCursor()
        # this doesn't do anything for now
        self.assertEqual(sys.stdout.read(), '')
        g.showCursor()

    def test_hide_cursor_no_clear_screen_linux(self):
        g = Game(scores_file=None, store_file=None, clear_screen=False)
        self.setWindows(g, False)
        g.hideCursor()
        self.assertEqual(sys.stdout.read(), '')

    def test_hide_cursor_no_clear_screen_windows(self):
        g = Game(scores_file=None, store_file=None, clear_screen=False)
        self.setWindows(g)
        g.hideCursor()
        self.assertEqual(sys.stdout.read(), '')

    # == .showCursor == #

    def test_show_cursor_linux(self):
        g = Game(scores_file=None, store_file=None, clear_screen=True)
        self.setWindows(g, False)
        g.hideCursor()
        g.showCursor()
        self.assertEqual(sys.stdout.read(), '\033[?25l\033[?25h')

    def test_show_cursor_windows(self):
        g = Game(scores_file=None, store_file=None, clear_screen=True)
        self.setWindows(g)
        g.hideCursor()
        g.showCursor()
        # these don't do anything for now
        self.assertEqual(sys.stdout.read(), '')

    def test_show_cursor_no_clear_screen_linux(self):
        g = Game(scores_file=None, store_file=None, clear_screen=False)
        self.setWindows(g, False)
        g.hideCursor()
        g.showCursor()
        self.assertEqual(sys.stdout.read(), '\033[?25h')

    # == .loop == #

    def test_simple_win_loop(self):
        kp._setNextKey(kp.UP)
        g = Game(goal=4, size=2, clear_screen=False)
        g.board.cells = [
            [2, 0],
            [2, 0]
        ]
        self.assertEqual(4, g.loop())

    def test_simple_win_loop_clear(self):
        kp._setNextKey(kp.UP)
        g = Game(goal=4, size=2, scores_file=None)
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
        g = Game(goal=4, size=2, scores_file=None)
        self.assertEqual(g.loop(), None)

    def test_loop_pause(self):
        store = NamedTemporaryFile(delete=False)
        store.close()
        kp._setNextKey(kp.SPACE)
        g = Game(scores_file=None, store_file=store.name)
        self.assertEqual(g.loop(), 0)
        self.assertFileIsNotEmpty(store.name)
        remove(store.name)

    def test_loop_pause_error(self):
        store = NamedTemporaryFile(delete=False)
        store.close()
        os.chmod(store.name, 0)  # no rights at all
        kp._setNextKey(kp.SPACE)
        g = Game(scores_file=None, store_file=store.name)
        self.assertIs(None, g.loop())
        os.chmod(store.name, 0o200)  # give me writing rights back
        remove(store.name)

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
