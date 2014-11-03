# -*- coding: UTF-8 -*-
try:
    import unittest2 as unittest
except ImportError:
    import unittest

import os
import sys
from os import remove
from tempfile import NamedTemporaryFile

import helpers
from term2048 import ui
from term2048.game import Game

_argv = sys.argv
_os_system = os.system
_game_loop = Game.loop
_store_file = Game.STORE_FILE

class TestUI(unittest.TestCase):

    def setUp(self):
        store = NamedTemporaryFile(delete=False)
        self.exit_status = None
        def fake_exit(s):
            self.exit_status = s
            raise helpers.FakeExit()
        self.exit = sys.exit
        sys.exit = fake_exit
        sys.argv = _argv
        self.stdout = sys.stdout
        self.output = helpers.DevNull()
        self._game_loop_started = False
        def _loop(*args, **kwargs):
            self._game_loop_started = True
        Game.loop = _loop
        Game.STORE_FILE = store.name
        sys.stdout = self.output

    def tearDown(self):
        sys.exit = self.exit
        sys.stdout = self.stdout
        Game.loop = _game_loop
        remove(Game.STORE_FILE)
        Game.STORE_FILE = _store_file

    def test_print_version(self):
        try:
            ui.print_version_and_exit()
        except helpers.FakeExit:
            pass
        else:
            self.assertFalse(True, "should exit after printing the version")
        self.assertEqual(self.exit_status, 0)

    def test_print_rules(self):
        try:
            ui.print_rules_and_exit()
        except helpers.FakeExit:
            pass
        else:
            self.assertFalse(True, "should exit after printing the rules")
        self.assertEqual(self.exit_status, 0)

    def test_parse_args_no_args(self):
        sys.argv = ['term2048']
        args = ui.parse_cli_args()
        self.assertEqual(args, {
            'version': False,
            'azmode': False,
            'mode': None,
            'rules': False,
            'resume': False,
        })

    def test_parse_args_version_long(self):
        sys.argv = ['term2048', '--version']
        args = ui.parse_cli_args()
        self.assertTrue(args['version'])

    def test_parse_args_version_short(self):
        sys.argv = ['term2048', '-v']
        args = ui.parse_cli_args()
        self.assertTrue(args['version'])

    def test_parse_args_azmode(self):
        sys.argv = ['term2048', '--az']
        args = ui.parse_cli_args()
        self.assertTrue(args['azmode'])

    def test_parse_args_azmode_version(self):
        sys.argv = ['term2048', '--az', '--version']
        args = ui.parse_cli_args()
        self.assertTrue(args['azmode'])
        self.assertTrue(args['version'])

    def test_parse_args_rules_version(self):
        sys.argv = ['term2048', '--rules', '--version']
        args = ui.parse_cli_args()
        self.assertTrue(args['rules'])
        self.assertTrue(args['version'])

    def test_parse_args_rules_short(self):
        sys.argv = ['term2048', '-r']
        args = ui.parse_cli_args()
        self.assertTrue(args['rules'])

    def test_parse_args_rules_version_short_rv(self):
        sys.argv = ['term2048', '-rv']
        args = ui.parse_cli_args()
        self.assertTrue(args['rules'])
        self.assertTrue(args['version'])

    def test_parse_args_rules_version_short_vr(self):
        sys.argv = ['term2048', '-vr']
        args = ui.parse_cli_args()
        self.assertTrue(args['rules'])
        self.assertTrue(args['version'])

    def test_parse_args_dark_mode(self):
        m = 'dark'
        sys.argv = ['term2048', '--mode', m]
        args = ui.parse_cli_args()
        self.assertEqual(args['mode'], m)

    def test_parse_args_light_mode(self):
        m = 'light'
        sys.argv = ['term2048', '--mode', m]
        args = ui.parse_cli_args()
        self.assertEqual(args['mode'], m)

    def test_start_game_print_version(self):
        sys.argv = ['term2048', '--version']
        try:
            ui.start_game()
        except helpers.FakeExit:
            pass
        else:
            self.assertFalse(True, "should exit after printing the version")
        self.assertEqual(self.exit_status, 0)
        self.assertRegexpMatches(self.output.read(),
                r'^term2048 v\d+\.\d+\.\d+$')

    def test_start_game_print_version_over_rules(self):
        sys.argv = ['term2048', '--rules', '--version']
        try:
            ui.start_game()
        except helpers.FakeExit:
            pass
        else:
            self.assertFalse(True, "should exit after printing the version")
        self.assertEqual(self.exit_status, 0)
        self.assertRegexpMatches(self.output.read(),
                r'^term2048 v\d+\.\d+\.\d+$')

    def test_start_game_print_rules(self):
        sys.argv = ['term2048', '--rules']
        try:
            ui.start_game()
        except helpers.FakeExit:
            pass
        else:
            self.assertFalse(True, "should exit after printing the version")
        self.assertEqual(self.exit_status, 0)
        self.assertRegexpMatches(self.output.read(), r'.+')

    def test_start_game_loop(self):
        sys.argv = ['term2048']
        self.assertFalse(self._game_loop_started)
        ui.start_game()
        self.assertTrue(self._game_loop_started)

    def test_start_game_no_resume(self):
        g1 = Game(scores_file=None)
        g1.board.setCell(0, 0, 16)
        self.assertTrue(g1.store())

        sys.argv = ['term2048']
        g2 = ui.start_game(debug=True)
        self.assertIn(g2.board.getCell(0, 0), [0, 2, 4])

    def test_start_game_resume(self):
        cellvalue = 2
        g1 = Game(scores_file=None)
        g1.board.setCell(0, 0, cellvalue)
        g1.score = 42
        self.assertTrue(g1.store())

        sys.argv = ['term2048', '--resume']
        g2 = ui.start_game(debug=True)
        self.assertEqual(cellvalue, g2.board.getCell(0, 0))
        self.assertEqual(g1.score, g2.score)
