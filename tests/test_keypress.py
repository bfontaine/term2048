# -*- coding: UTF-8 -*-

import sys
import platform

if platform.python_version() < '3.0':
    from StringIO import StringIO
else:
    from io import StringIO

if platform.python_version() < '2.7':
    import unittest2 as unittest
else:
    import unittest

try:
    import termios as _termios
except ImportError:
    _termios = None

import helpers
from term2048 import keypress as kp
keypress = kp._getRealModule()

fno = sys.stdin.fileno()


class FakeStdin(StringIO):
    def fileno(self):
        return fno


class TestKeypress(unittest.TestCase):

    def _pushChars(self, *chars):
        """helper. Add chars in the fake stdin"""
        sys.stdin.write(''.join(map(chr, chars)))
        sys.stdin.seek(0)

    def _pushArrowKey(self, code):
        """helper. Add an arrow special key in the fake stdin"""
        self._pushChars(27, 91, code)

    def setUp(self):
        self.stdin = sys.stdin
        sys.stdin = FakeStdin()

    def tearDown(self):
        sys.stdin = self.stdin

    def test_getKey_read_stdin(self):
        x = 42
        self._pushChars(x)
        self.assertEqual(keypress.getKey(), x)

    def test_getKey_arrow_key_up(self):
        k = keypress.UP
        self._pushArrowKey(k)
        self.assertEqual(keypress.getKey(), k)

    def test_getKey_arrow_key_down(self):
        k = keypress.DOWN
        self._pushArrowKey(k)
        self.assertEqual(keypress.getKey(), k)

    def test_getKey_arrow_key_left(self):
        k = keypress.LEFT
        self._pushArrowKey(k)
        self.assertEqual(keypress.getKey(), k)

    def test_getKey_arrow_key_right(self):
        k = keypress.RIGHT
        self._pushArrowKey(k)
        self.assertEqual(keypress.getKey(), k)

    def test_getKey_vim_key_up(self):
        self._pushChars(keypress.K)
        self.assertEqual(keypress.getKey(), keypress.UP)

    def test_getKey_vim_key_down(self):
        self._pushArrowKey(keypress.J)
        self.assertEqual(keypress.getKey(), keypress.DOWN)

    def test_getKey_vim_key_left(self):
        self._pushArrowKey(keypress.H)
        self.assertEqual(keypress.getKey(), keypress.LEFT)

    def test_getKey_vim_key_right(self):
        self._pushArrowKey(keypress.L)
        self.assertEqual(keypress.getKey(), keypress.RIGHT)


class TestKeypressWindows(unittest.TestCase):

    def setUp(self):
        sys.modules['termios'] = None
        sys.modules['msvcrt'] = helpers.FakeMsvcrt()
        helpers.reload(keypress)

    def tearDown(self):
        sys.modules['termios'] = _termios

    def test_termios_fallback_on_msvcrt(self):
        self.assertEqual(keypress.UP, 72)

    def test_termios_fallback_on_msvcrt_getKey(self):
        self.assertEqual(keypress.getKey(), helpers.msvcrt_key)
