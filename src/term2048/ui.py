#! /usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import keypress
from board import Board

dirs = {
    keypress.UP:    Board.UP,
    keypress.DOWN:  Board.DOWN,
    keypress.LEFT:  Board.LEFT,
    keypress.RIGHT: Board.RIGHT
}

def start_game():
    b = Board()
    while not b.won() and b.canMove():
        os.system('cls' if os.name == 'nt' else 'clear')
        print b
        k = keypress.getArrowKey()
        d = dirs.get(k)
        if d == None:
            continue
        b.move(d)

    print 'You won!' if b.won() else 'Game Over'

if __name__ == '__main__':
    start_game()
