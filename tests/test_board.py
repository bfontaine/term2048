# -*- coding: UTF-8 -*-

import unittest
from term2048.board import Board

class TestBoard(unittest.TestCase):

    def setUp(self):
        self.b = Board()

    # == init == #
    def test_init_dimensions(self):
        self.assertEqual(len(self.b.cells), Board.SIZE)
        self.assertEqual(len(self.b.cells[0]), Board.SIZE)
        if Board.SIZE > 1:
            self.assertEqual(len(self.b.cells[1]), Board.SIZE)

    def test_init_dimensions_1(self):
        b = Board(size=1)
        c = b.cells[0][0]
        self.assertTrue(c in [2, 4])

    def test_init_dimensions_3_goal_4(self):
        b = Board(size=3, goal=4)
        self.assertEqual(b.size(), 3)

    def test_init_only_two_tiles(self):
        t = 0
        for x in xrange(Board.SIZE):
            for y in xrange(Board.SIZE):
                c = self.b.cells[y][x]
                if not c == 0:
                    t += 1
                else:
                    self.assertEqual(c, 0, 'board[%d][%d] should be 0' % (y, x))

        self.assertEqual(t, 2)

    def test_init_not_won(self):
        self.assertFalse(self.b.won())

    def test_init_not_filled(self):
        self.assertFalse(self.b.filled())

    # == .size == #
    def test_size(self):
        s = 42
        b = Board(size=s)
        self.assertEqual(b.size(), s)

    # == .won == #
    def test_won(self):
        self.b._Board__won = True
        self.assertTrue(self.b.won())
        self.b._Board__won = False
        self.assertFalse(self.b.won())

    # == .canMove == #
    def test_canMove_no_empty_cell(self):
        b = Board(size=1)
        b.setCell(0, 0, 42)
        self.assertFalse(b.canMove())

    def test_canMove_empty_cell(self):
        b = Board(size=2)
        self.assertTrue(b.canMove())

    def test_canMove_no_empty_cell_can_collapse(self):
        b = Board(size=2)
        b.cells = [
            [2, 2],
            [4, 8]
        ]
        self.assertTrue(b.canMove())

    # == .filled == #
    def test_filled(self):
        self.b.cells = [[1]*Board.SIZE for _ in xrange(Board.SIZE)]
        self.assertTrue(self.b.filled())

    # == .addTile == #
    def test_addTile(self):
        b = Board(size=1)
        b.cells = [[0]]
        b.addTile(value=42)
        self.assertEqual(b.cells[0][0], 42)

    # == .getCell == #
    def test_getCell(self):
        x, y = 3, 1
        v = 42
        self.b.cells[y][x] = v
        self.assertEqual(self.b.getCell(x, y), v)

    # == .setCell == #
    def test_setCell(self):
        x, y = 2, 3
        v = 42
        self.b.setCell(x, y, v)
        self.assertEqual(self.b.cells[y][x], v)

    # == .getLine == #
    def test_getLine(self):
        b = Board(size=4)
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
        s = 4
        b = Board(size=s)
        l = [42, 17, 12, 3]
        b.cells = [[l[i], 4, 1, 2] for i in xrange(s)]
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
        b = Board(size=1)
        b.setCell(0, 0, 42)
        self.assertSequenceEqual(b.getEmptyCells(), [])

    # == .move == #
    def test_move_filled(self):
        b = Board(size=1)
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
        b = Board(size=1)
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
        b = Board(size=2)
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
        b = Board(size=3)
        b.setLine(0, [2, 2, 2])
        b.move(Board.LEFT, add_tile=False)
        self.assertSequenceEqual(b.getLine(0), [4, 2, 0])

    def test_move_collapse_triplet2(self):
        b = Board(size=3)
        b.setLine(0, [2, 2, 2])
        b.move(Board.RIGHT, add_tile=False)
        self.assertSequenceEqual(b.getLine(0), [0, 2, 4])

    def test_move_collapse_with_empty_cell_in_between(self):
        b = Board(size=3)
        b.setLine(0, [2, 0, 2])
        b.move(Board.RIGHT, add_tile=False)
        self.assertSequenceEqual(b.getLine(0), [0, 0, 4])

    def test_move_collapse_with_empty_cell_in_between2(self):
        b = Board(size=3)
        b.setLine(0, [2, 0, 2])
        b.move(Board.LEFT, add_tile=False)
        self.assertSequenceEqual(b.getLine(0), [4, 0, 0])

    def test_move_collapse_and_win(self):
        b = Board(size=2, goal=4)
        b.cells = [
            [2, 2],
            [0, 0]
        ]
        b.move(Board.LEFT, add_tile=False)
        self.assertTrue(b.won())

    def test_move_wrong_direction(self):
        self.assertEqual(self.b.move(42, add_tile=False), 0)
        self.assertEqual(self.b.move(None), 0)
        self.assertEqual(self.b.move("up"), 0)

    def test_move_collapse_chain_col(self):
        # from https://news.ycombinator.com/item?id=7398249
        b = Board()
        b.setCol(0, [0, 2, 2, 4])
        b.move(Board.DOWN, add_tile=False)
        self.assertSequenceEqual(b.getCol(0), [0, 0, 4, 4])

    def test_move_collapse_chain_line(self):
        # from https://news.ycombinator.com/item?id=7398249
        b = Board()
        b.cells = [
            [0, 2, 2, 4],
            [0]*4,
            [0]*4,
            [0]*4
        ]
        self.assertEqual(b.move(Board.RIGHT, add_tile=False), 4)
        self.assertSequenceEqual(b.getLine(0), [0, 0, 4, 4])
