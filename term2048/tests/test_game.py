# -*- coding: UTF-8 -*-
try:
    import unittest2 as unittest
except ImportError:
    import unittest

import keypress_mock as kp
from colorama import Fore, Style
from term2048.board import Board
from term2048.game import Game

import sys
import os
from helpers import DevNull

_BSIZE = Board.SIZE

class TestGame(unittest.TestCase):

    def setUp(self):
        Board.SIZE = _BSIZE
        self.g = Game()
        self.b = self.g.board
        # don't print anything on stdout
        self.stdout = sys.stdout
        sys.stdout = DevNull()
        # mock os.system
        self.system = os.system
        self.sys_cmd = None
        def fake_system(*cmd):
            self.sys_cmd = cmd

        os.system = fake_system

    def tearDown(self):
        sys.stdout = self.stdout
        os.system = self.system
        kp._setCtrlC(False)

    def test_init_with_size_3_goal_4(self):
        g = Game(size=3, goal=4)
        self.assertEqual(g.board.size(), 3)

    # == .incScore == #

    def test_inc_0_score(self):
        s = 3
        self.g.score = s
        self.g.incScore(0)
        self.assertEqual(self.g.score, s)

    def test_inc_2_score(self):
        s = 3
        i = 2
        self.g.score = s
        self.g.incScore(i)
        self.assertEqual(self.g.score, s+i)

    # == .end == #

    def test_end_can_play(self):
        self.assertFalse(self.g.end())

    # == .readMove == #

    def test_read_unknown_move(self):
        kp._setNextKey(-1)
        self.assertEqual(self.g.readMove(), None)

    def test_read_known_move(self):
        kp._setNextKey(kp.LEFT)
        self.assertEqual(self.g.readMove(), Board.LEFT)

    # == .loop == #

    def test_simple_win_loop(self):
        kp._setNextKey(kp.UP)
        g = Game(goal=4, size=2)
        g.board.cells = [
            [2, 0],
            [2, 0]
        ]
        g.loop()

    def test_simple_win_loop_clear(self):
        kp._setNextKey(kp.UP)
        g = Game(goal=4, size=2)
        g.board.cells = [
            [2, 0],
            [2, 0]
        ]
        self.assertEqual(g.loop(), 4)
        if os.name == 'nt':
            self.assertEqual(self.sys_cmd, ('cls',))
        else:
            self.assertEqual(self.sys_cmd, ('clear',))

    def test_loop_interrupt(self):
        kp._setCtrlC(True)
        g = Game(goal=4, size=2)
        self.assertEqual(g.loop(), None)

    # == .getCellStr == #

    def test_getCellStr_0(self):
        self.b.setCell(0, 0, 0)
        self.assertEqual(self.g.getCellStr(0, 0), '  .')

    def test_getCellStr_unknown_number(self):
        self.b.setCell(0, 0, 42)
        self.assertEqual(self.g.getCellStr(0, 0),
                '%s 42%s' % (Fore.RESET, Style.RESET_ALL))

    def test_getCellStr_2(self):
        g = Game()
        g.board.setCell(0, 0, 2)
        self.assertRegexpMatches(g.getCellStr(0, 0), r'  2\x1b\[0m$')

    def test_getCellStr_1k(self):
        g = Game()
        g.board.setCell(0, 0, 1024)
        self.assertRegexpMatches(g.getCellStr(0, 0), r' 1k\x1b\[0m$')

    def test_getCellStr_2k(self):
        g = Game()
        g.board.setCell(0, 0, 2048)
        self.assertRegexpMatches(g.getCellStr(0, 0), r' 2k\x1b\[0m$')

    # == .boardToString == #

    def test_boardToString_height_no_margins(self):
        s = self.g.boardToString()
        self.assertEqual(len(s.split("\n")), self.b.size())

    # == .__str__ == #

    def test_str_height_no_margins(self):
        s = str(self.g)
        self.assertEqual(len(s.split("\n")), self.b.size())
