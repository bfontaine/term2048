# -*- coding: UTF-8 -*-
try:
    import unittest2 as unittest
except ImportError:
    import unittest

import sys
from term2048 import ui
from helpers import DevNull

class TestUI(unittest.TestCase):

    def setUp(self):
        self.exit_status = None
        def fake_exit(s):
            self.exit_status = s
        self.exit = sys.exit
        sys.exit = fake_exit
        self.stdout = sys.stdout
        sys.stdout = DevNull()

    def tearDown(self):
        sys.exit = self.exit
        sys.stdout = self.stdout

    def test_print_version(self):
        ui.print_version_and_exit()
        self.assertEqual(self.exit_status, 0)
