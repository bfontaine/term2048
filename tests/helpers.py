# -*- coding: UTF-8 -*-

import platform

msvcrt_key = 42

# use this for mocking stdout
class DevNull(object):
    def write(self, *args):
        pass

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
