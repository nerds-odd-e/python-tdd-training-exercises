# -*- coding: UTF-8 -*-
from __future__ import print_function

import os

from colorama import init, Fore, Style
init(autoreset=True)

from term2048 import keypress
from term2048.board import Board


class Game(object):
    """
    A 2048 game
    """

    __dirs = {
        keypress.UP:      Board.UP,
        keypress.DOWN:    Board.DOWN,
        keypress.LEFT:    Board.LEFT,
        keypress.RIGHT:   Board.RIGHT,
    }

    __clear = 'cls' if os.name == 'nt' else 'clear'

    def __init__(self, **kws):
        """
        Create a new game.
        """
        self.board = Board(**kws)
        self.score = 0
        self.__colors = {
            2:    Fore.GREEN,
            4:    Fore.BLUE + Style.BRIGHT,
            8:    Fore.CYAN,
            16:   Fore.RED,
            32:   Fore.MAGENTA,
            64:   Fore.CYAN,
            128:  Fore.BLUE + Style.BRIGHT,
            256:  Fore.MAGENTA,
            512:  Fore.GREEN,
            1024: Fore.RED,
            2048: Fore.YELLOW,
            # just in case people set an higher goal they still have colors
            4096: Fore.RED,
            8192: Fore.CYAN,
        }

    def incScore(self, pts):
        """
        update the current score by adding it the specified number of points
        """
        self.score += pts

    def end(self):
        """
        return True if the game is finished
        """
        return not (self.board.won() or self.board.canMove())

    def readMove(self):
        """
        read and return a move to pass to a board
        """
        k = keypress.getKey()
        return Game.__dirs.get(k)

    def loop(self):
        """
        main game loop. returns the final score.
        """
        try:
            while True:
                os.system(Game.__clear)
                print(self.__str__(margins={'left': 4, 'top': 4, 'bottom': 4}))
                if self.board.won() or not self.board.canMove():
                    break
                m = self.readMove()
                self.incScore(self.board.move(m))

        except KeyboardInterrupt:
            return

        print('You won!' if self.board.won() else 'Game Over')
        return self.score

    def getCellStr(self, x, y):  # TODO: refactor regarding issue #11
        """
        return a string representation of the cell located at x,y.
        """
        c = self.board.getCell(x, y)

        if c == 0:
            return '  .'
        elif c == 1024:
            s = ' 1k'
        elif c == 2048:
            s = ' 2k'
        else:
            s = '%3d' % c

        return self.__colors.get(c, Fore.RESET) + s + Style.RESET_ALL

    def boardToString(self, margins={}):
        """
        return a string representation of the current board.
        """
        b = self.board
        rg = range(b.size())
        left = ' '*margins.get('left', 0)
        s = '\n'.join(
            [left + ' '.join([self.getCellStr(x, y) for x in rg]) for y in rg])
        return s

    def __str__(self, margins={}):
        b = self.boardToString(margins=margins)
        top = '\n'*margins.get('top', 0)
        bottom = '\n'*margins.get('bottom', 0)
        scores = ' \tScore: %5d\n' % (self.score)
        return top + b.replace('\n', scores, 1) + bottom
