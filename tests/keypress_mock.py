# -*- coding: UTF-8 -*-

# helpers

__kp = None
__keys = []
__ctrl_c = False # flag for KeyboardInterrupt

UP, DOWN, LEFT, RIGHT, SPACE = range(5)

def _setRealModule(m):
    """test helper, save the real keypress module"""
    global __kp, UP, DOWN, LEFT, RIGHT, SPACE
    __kp=m
    UP = __kp.UP
    DOWN = __kp.DOWN
    LEFT = __kp.LEFT
    RIGHT = __kp.RIGHT
    SPACE = __kp.SPACE

def _getRealModule():
    return __kp

def _setNextKeys(ks):
    """test helper, set next key to return with getKey"""
    global __keys
    __keys = ks

def _setNextKey(k):
    _setNextKeys([k])

def _setCtrlC(yes=True):
    global __ctrl_c
    __ctrl_c = yes

# mocks

def getKey():
    """mock term2048.keypress.getKey"""
    if __ctrl_c:
        raise KeyboardInterrupt()
    return __keys.pop()
