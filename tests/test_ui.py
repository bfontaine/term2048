# -*- coding: UTF-8 -*-
try:
    import unittest2 as unittest
except ImportError:
    import unittest

import sys
from term2048 import ui
from helpers import DevNull

_argv = sys.argv

class TestUI(unittest.TestCase):

    def setUp(self):
        self.exit_status = None
        def fake_exit(s):
            self.exit_status = s
        self.exit = sys.exit
        sys.exit = fake_exit
        self.stdout = sys.stdout
        self.output = {}
        sys.argv = _argv
        sys.stdout = DevNull(self.output)

    def tearDown(self):
        sys.exit = self.exit
        sys.stdout = self.stdout

    def test_print_version(self):
        ui.print_version_and_exit()
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
