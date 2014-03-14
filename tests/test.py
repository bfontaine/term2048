# -*- coding: UTF-8 -*-
import sys

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from os.path import dirname

if __name__ == '__main__':
    here = dirname(__file__)
    sys.path.insert(0, here+'/..')
    suite = unittest.defaultTestLoader.discover(here)
    t = unittest.TextTestRunner().run(suite)
    if not t.wasSuccessful():
        sys.exit(1)
