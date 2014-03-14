# -*- coding: UTF-8 -*-

try:
    import termios
except ImportError:
    # Assume windows
    
    import msvcrt
    
    LEFT, UP, RIGHT, DOWN = 75, 72, 77, 80
    
    def getKey():
        while True:
            if msvcrt.kbhit():
                a = ord(msvcrt.getch())
                return a
    
    getArrowKey = getKey
else:
    # refs:
    # http://bytes.com/topic/python/answers/630206-check-keypress-linux-xterm
    # http://stackoverflow.com/a/2521032/735926
    
    import sys
    import tty
    
    __fd = sys.stdin.fileno()
    __old = termios.tcgetattr(__fd)

    # up: 27 91 65
    # down: 27 91 66
    # left: 27 91 68
    # right: 27 91 67
    UP, DOWN, RIGHT, LEFT = 65, 66, 67, 68

    def getKey():
        """Return a key pressed by the user"""
        try:
            tty.setcbreak(sys.stdin.fileno())
            termios.tcflush(sys.stdin, termios.TCIOFLUSH)
            ch = sys.stdin.read(1)
            return ord(ch)
        finally:
            termios.tcsetattr(__fd, termios.TCSADRAIN, __old)


    def getArrowKey():
        """same as getKey, but assuming that the user pressed an arrow key"""
        k = getKey()
        if not k in hjkl:
            getKey()
            return getKey()
        else:
            return k

UP_K, DOWN_J, RIGHT_L, LEFT_H = 107, 106, 108, 104
hjkl = (UP_K, DOWN_J, RIGHT_L, LEFT_H)
