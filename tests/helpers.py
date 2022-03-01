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
python_version = platform.python_version()
if python_version < '3.0':
    reload = reload
elif '3.2' <= python_version < '3.4':
    import imp

    reload = imp.reload
else:
    import importlib

    reload = importlib.reload


# used by sys.exit mocks
class FakeExit(Exception):
    pass
