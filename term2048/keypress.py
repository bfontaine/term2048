# -*- coding: UTF-8 -*-

# refs:
# http://bytes.com/topic/python/answers/630206-check-keypress-linux-xterm
# http://stackoverflow.com/a/2521032/735926

import sys
import tty
import termios

__fd = sys.stdin.fileno()
__old = termios.tcgetattr(__fd)

# up: 27 91 65
# down: 27 91 66
# left: 27 91 68
# right: 27 91 67
UP, DOWN, RIGHT, LEFT = 65, 66, 67, 68
UP_K, DOWN_J, RIGHT_L, LEFT_H = 107, 106, 108, 104
hjkl = (107, 106, 108, 104)


def __getKey():
    """Return a key pressed by the user"""
    try:
        tty.setcbreak(sys.stdin.fileno())
        termios.tcflush(sys.stdin, termios.TCIOFLUSH)
        ch = sys.stdin.read(1)
        return ord(ch)
    finally:
        termios.tcsetattr(__fd, termios.TCSADRAIN, __old)


def getKey():
    """
    same as __getKey, but handle arrow keys
    """
    k = __getKey()
    if k == 27:
        k = __getKey()
        if k == 91:
            k = __getKey()

    return k

def getArrowKey():
    """legacy function. See getKey"""
    return getKey()
