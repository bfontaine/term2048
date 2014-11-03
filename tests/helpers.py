# -*- coding: UTF-8 -*-

import platform

msvcrt_key = 42

# use this for mocking stdout
class DevNull(object):
    def __init__(self):
        self.output = ''

    def write(self, s):
        self.output += s

    def read(self):
        return self.output[:]

# use this for mocking msvcrt
class FakeMsvcrt(object):
    def kbhit(self):
        return True
    def getch(self):
        return chr(msvcrt_key)

# builtin (before 3.0) function 'reload(<module>)'
if platform.python_version() < '3.0':
    reload = reload
else:
    import imp
    reload = imp.reload

# used by sys.exit mocks
class FakeExit(Exception):
    pass
