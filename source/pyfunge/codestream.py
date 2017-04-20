""" コードモジュール。

2017/4/16 masaniwa
"""

from enum import Enum


class CodeStream:
    """ コード。
    """

    def __init__(self, code):
        self.__code = code.split("\n")

        self.__initialize()

    def __iter__(self):
        self.__initialize()

        return self

    def __next__(self):
        if not self.__continuation:
            raise StopIteration()

        if self.__skipping:
            self.__move()

        self.__skipping = False

        self.__move()

        character = self.__code[self.__row][self.__col]

        return character

    def change_direction(self, direction):
        """ コードを読み取る方向を変える。
        """

        if direction == Direction.right:
            self.__row_movement = 0
            self.__col_movement = 1

        elif direction == Direction.left:
            self.__row_movement = 0
            self.__col_movement = -1

        elif direction == Direction.down:
            self.__row_movement = 1
            self.__col_movement = 0

        else:
            self.__row_movement = -1
            self.__col_movement = 0

    def skip(self):
        """ コードを1文字飛ばす。
        """

        self.__skipping = True

    def stop(self):
        """ コードの読み取りを終了する。
        """
        self.__continuation = False

    def read_char(self, row, col):
        """ コード上の座標の文字を返す。
        """

        return self.__code[row][col]

    def write_char(self, row, col, character):
        """ コード上の座標の文字を書き換える。
        """

        before = self.__code[row][:col]
        after = self.__code[row][col + 1:]

        self.__code[row] = before + character + after

    def __initialize(self):
        """ 初期化する。
        """

        last = 1 if len(self.__code[-1]) == 0 else 0

        self.__row = 0
        self.__col = -1
        self.__rows = len(self.__code) - last
        self.__cols = len(self.__code[0])
        self.__row_movement = 0
        self.__col_movement = 1

        self.__skipping = False
        self.__continuation = True

    def __move(self):
        """ コード上を移動する。
        """

        row = self.__row + self.__row_movement
        col = self.__col + self.__col_movement

        self.__row = self.__circulate(row, 0, self.__rows - 1)
        self.__col = self.__circulate(col, 0, self.__cols - 1)

    @classmethod
    def __circulate(cls, number, lower, upper):
        """ 数を範囲内で循環させて返す。
        """

        if lower <= number <= upper:
            return number

        elif number < lower:
            return cls.__circulate(upper + lower + number + 1, lower, upper)

        else:
            return cls.__circulate(lower + number - upper - 1, lower, upper)


class Direction(Enum):
    """ 方向。
    """

    up = 0
    down = 1
    right = 2
    left = 3