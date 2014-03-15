# -*- coding: UTF-8 -*-
try:
    import unittest2 as unittest
except ImportError:
    import unittest

import sys
import os
import helpers
from term2048 import ui

try:
    import argparse as _argparse
except ImportError:
    _argparse = None

_argv = sys.argv
_os_system = os.system

class TestUI(unittest.TestCase):

    def setUp(self):
        self.exit_status = None
        def fake_exit(s):
            self.exit_status = s
            raise helpers.FakeExit()
        self.exit = sys.exit
        sys.exit = fake_exit
        sys.argv = _argv
        self.stdout = sys.stdout
        self.output = {}
        sys.stdout = helpers.DevNull(self.output)

    def tearDown(self):
        sys.exit = self.exit
        sys.stdout = self.stdout

    def test_print_version(self):
        try:
            ui.print_version_and_exit()
        except helpers.FakeExit:
            pass
        else:
            self.assertFalse(True, "should exit after printing the version")
        self.assertEqual(self.exit_status, 0)

    def test_parse_args_no_args(self):
        sys.argv = ['term2048']
        args = ui.parse_cli_args()
        self.assertEqual(args, {
            'version': False,
            'azmode': False,
            'mode': None,
        })

    def test_parse_args_version(self):
        sys.argv = ['term2048', '--version']
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

    def test_argparse_warning(self):
        getattr(ui, '__print_argparse_warning')()
        self.assertIn('output', self.output)
        self.assertRegexpMatches(self.output['output'], r'^WARNING')

    def test_start_game_print_version(self):
        sys.argv = ['term2048', '--version']
        try:
            ui.start_game()
        except helpers.FakeExit:
            pass
        else:
            self.assertFalse(True, "should exit after printing the version")
        self.assertEqual(self.exit_status, 0)
        self.assertRegexpMatches(self.output['output'],
                r'^term2048 v\d+\.\d+\.\d+$')

class TestUIPy26(unittest.TestCase):

    def setUp(self):
        self.stdout = sys.stdout
        self.output = {}
        sys.stdout = helpers.DevNull(self.output)
        sys.modules['argparse'] = None
        helpers.reload(ui)
        ui.debug = True
        def system_interrupt(*args):
            raise KeyboardInterrupt()
        os.system = system_interrupt

    def tearDown(self):
        sys.stdout = self.stdout
        sys.modules['argparse'] = _argparse
        ui.debug = False
        os.system = _os_system

    def test_no_has_argparse(self):
        self.assertFalse(getattr(ui, '__has_argparse'))

    def test_start_game_print_argparse_warning(self):
        ui.start_game()
        self.assertIn('output', self.output)
        self.assertRegexpMatches(self.output['output'], r'^WARNING')

    def test_start_game_loop(self):
        ui.debug = False
        self.assertEqual(ui.start_game(), None) # interrupted
