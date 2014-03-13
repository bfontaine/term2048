# -*- coding: UTF-8 -*-

import unittest
from term2048.board import Board

_BSIZE = Board.SIZE

class TestBoard(unittest.TestCase):

    def setUp(self):
        Board.SIZE = _BSIZE
        self.b = Board()

    # == init == #
    def test_init_dimensions(self):
        self.assertEqual(len(self.b.cells), Board.SIZE)
        self.assertEqual(len(self.b.cells[0]), Board.SIZE)
        if Board.SIZE > 1:
            self.assertEqual(len(self.b.cells[1]), Board.SIZE)

    def test_init_dimensions_1(self):
        Board.SIZE = 1
        b = Board()
        self.assertEqual(b.cells, [[2]])

    def test_init_only_two_tiles(self):
        t = 0
        for x in xrange(Board.SIZE):
            for y in xrange(Board.SIZE):
                c = self.b.cells[y][x]
                if c == 2:
                    t += 1
                else:
                    self.assertEqual(c, 0, 'board[%d][%d] should be 0' % (y, x))

        self.assertEqual(t, 2)

    def test_init_not_won(self):
        self.assertFalse(self.b.won())

    def test_init_not_filled(self):
        self.assertFalse(self.b.filled())

    # == .won == #
    def test_won(self):
        self.b._Board__won = True
        self.assertTrue(self.b.won())
        self.b._Board__won = False
        self.assertFalse(self.b.won())

    # == .filled == #
    def test_filled(self):
        self.b.cells = [[1]*Board.SIZE for _ in xrange(Board.SIZE)]
        self.assertTrue(self.b.filled())

    # == .addTile == #
    def test_addTile(self):
        Board.SIZE = 1
        b = Board()
        b.cells = [[0]]
        b.addTile(value=42)
        self.assertEqual(b.cells[0][0], 42)

    # == .getCell == #
    def test_getCell(self):
        x, y = 3, 1
        v = 42
        self.b.cells[y][x] = v
        self.assertEqual(self.b.getCell(x, y), v)

    # == .getCell == #
    def test_getCellStr_empty(self):
        x, y = 3, 1
        self.b.cells[y][x] = 0
        self.assertEqual(self.b.getCellStr(x, y), '   .')

    def test_getCellStr_2(self):
        x, y = 3, 1
        self.b.cells[y][x] = 2
        self.assertEqual(self.b.getCellStr(x, y), '   2')

    def test_getCellStr_2048(self):
        x, y = 3, 1
        self.b.cells[y][x] = 2048
        self.assertEqual(self.b.getCellStr(x, y), '2048')

    # == .setCell == #
    def test_setCell(self):
        x, y = 2, 3
        v = 42
        self.b.setCell(x, y, v)
        self.assertEqual(self.b.cells[y][x], v)

    # == .getLine == #
    def test_getLine(self):
        Board.SIZE = 4
        b = Board()
        l = [42, 17, 12, 3]
        b.cells = [
            [0]*4,
            l,
            [0]*4,
            [0]*4
        ]
        self.assertSequenceEqual(b.getLine(1), l)

    # == .getCol == #
    def test_getCol(self):
        Board.SIZE = 4
        b = Board()
        l = [42, 17, 12, 3]
        b.cells = [[l[i], 4, 1, 2] for i in xrange(Board.SIZE)]
        self.assertSequenceEqual(b.getCol(0), l)

    # == .setLine == #
    def test_setLine(self):
        i = 2
        l = [1, 2, 3, 4]
        self.b.setLine(i, l)
        self.assertEqual(self.b.getLine(i), l)

    # == .setCol == #
    def test_setLine(self):
        i = 2
        l = [1, 2, 3, 4]
        self.b.setCol(i, l)
        self.assertEqual(self.b.getCol(i), l)

    # == .getEmptyCells == #
    def test_getEmptyCells(self):
        self.assertEqual(len(self.b.getEmptyCells()), Board.SIZE**2 - 2)

    def test_getEmptyCells_filled(self):
        Board.SIZE = 1
        b = Board()
        b.setCell(0, 0, 42)
        self.assertSequenceEqual(b.getEmptyCells(), [])

    # == .move == #
    def test_move_filled(self):
        Board.SIZE = 1
        b = Board()
        b.setCell(0, 0, 42)
        b.move(Board.UP)
        self.assertSequenceEqual(b.cells, [[42]])
        b.move(Board.LEFT)
        self.assertSequenceEqual(b.cells, [[42]])
        b.move(Board.RIGHT)
        self.assertSequenceEqual(b.cells, [[42]])
        b.move(Board.DOWN)
        self.assertSequenceEqual(b.cells, [[42]])

    def test_move_add_tile(self):
        Board.SIZE = 1
        b = Board()
        b.cells = [[0]]
        b.move(Board.UP)
        self.assertTrue(b.getCell(0, 0) != 0)
        b.cells = [[0]]
        b.move(Board.DOWN)
        self.assertTrue(b.getCell(0, 0) != 0)
        b.cells = [[0]]
        b.move(Board.LEFT)
        self.assertTrue(b.getCell(0, 0) != 0)
        b.cells = [[0]]
        b.move(Board.RIGHT)
        self.assertTrue(b.getCell(0, 0) != 0)

    def test_move_collapse(self):
        Board.SIZE = 2
        b = Board()
        b.cells = [
            [2, 2],
            [0, 0]
        ]

        b.move(Board.LEFT, add_tile=False)
        self.assertSequenceEqual(b.cells, [
            [4, 0],
            [0, 0]
        ])

    def test_move_collapse_triplet1(self):
        Board.SIZE = 3
        b = Board()
        b.setLine(0, [2, 2, 2])
        b.move(Board.LEFT, add_tile=False)
        self.assertSequenceEqual(b.getLine(0), [4, 2, 0])

    def test_move_collapse_triplet2(self):
        Board.SIZE = 3
        b = Board()
        b.setLine(0, [2, 2, 2])
        b.move(Board.RIGHT, add_tile=False)
        self.assertSequenceEqual(b.getLine(0), [0, 2, 4])

    def test_move_collapse_with_empty_cell_in_between(self):
        Board.SIZE = 3
        b = Board()
        b.setLine(0, [2, 0, 2])
        b.move(Board.RIGHT, add_tile=False)
        self.assertSequenceEqual(b.getLine(0), [0, 0, 4])

    def test_move_collapse_with_empty_cell_in_between2(self):
        Board.SIZE = 3
        b = Board()
        b.setLine(0, [2, 0, 2])
        b.move(Board.LEFT, add_tile=False)
        self.assertSequenceEqual(b.getLine(0), [4, 0, 0])

    # == .__str__ == #
    def test_str(self):
        Board.SIZE = 1
        b = Board()
        b.setCell(0, 0, 2048)
        self.assertEqual(b.__str__(), b.getCellStr(0, 0))
