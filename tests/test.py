# -*- coding: UTF-8 -*-

from os.path import dirname
import sys
import unittest

if __name__ == '__main__':
    here = dirname(__file__)
    sys.path.append(here+'/../src')
    suite = unittest.defaultTestLoader.discover(here)
    unittest.TextTestRunner().run(suite)
