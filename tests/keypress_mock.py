# -*- coding: UTF-8 -*-

# helpers

__kp = None
__keys = []

UP, DOWN, LEFT, RIGHT = range(4)

def _setRealModule(m):
    """test helper, save the real keypress module"""
    __kp=m
    UP = __kp.UP
    DOWN = __kp.DOWN
    LEFT = __kp.LEFT
    LEFT = __kp.LEFT

def _setNextKeys(ks):
    """test helper, set next key to return with getKey"""
    global __keys
    __keys = ks

def _setNextKey(k):
    _setNextKeys([k])

# mocks

def getKey():
    """mock term2048.keypress.getKey"""
    return __keys.pop()
