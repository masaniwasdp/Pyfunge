""" コードモジュール。

Date: 2017/7/15
Authors: masaniwa
"""

from enum import Enum
from typing import Iterable # flake8: noqa


class Direction(Enum):
    """ 方向。
    """

    up = 0
    down = 1
    right = 2
    left = 3


class CodeStream(Iterable):
    """ コード。
    """

    def __init__(self, code: str) -> None:
        """ 初期化をする。

        Params:
            code = 空でないBefungeのコード。

        Throws:
            RuntimeError コードの形が正しくない場合。
        """

        assert len(code) > 0

        self.__code = code.split("\n")[:-1]

        self.__check_code()

        self.__rows = len(self.__code)
        self.__cols = len(self.__code[0])

        self.__row = 0
        self.__col = -1
        self.__row_movement = 0
        self.__col_movement = 1

        self.__skippable = False
        self.__continuation = True

    def __iter__(self):
        self.__row = 0
        self.__col = -1
        self.__row_movement = 0
        self.__col_movement = 1

        self.__skippable = False
        self.__continuation = True

        return self

    def __next__(self) -> str:
        if not self.__continuation:
            raise StopIteration()

        if self.__skippable:
            self.__move()

            self.__skippable = False

        self.__move()

        return self.__code[self.__row][self.__col]

    def change_direction(self, direction: Direction) -> None:
        """ コードを読み取る方向を変える。

        Params:
            direction = 読み取る方向。
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

    def skip(self) -> None:
        """ コードを1文字飛ばす。
        """

        self.__skippable = True

    def stop(self) -> None:
        """ コードの読み取りを終了する。
        """
        self.__continuation = False

    def read_char(self, row: int, col: int) -> str:
        """ コード上の文字を読む。

        Params:
            row = 行。
            col = 列。

        Returns: 読み取った文字。

        Throws:
            RuntimeError 位置がコード外だった場合。
        """

        assert row >= 0
        assert col >= 0

        if row >= len(self.__code) or col >= len(self.__code[row]):
            raise RuntimeError("The index was out of bounds.")

        return self.__code[row][col]

    def write_char(self, row: int, col: int, character: str) -> None:
        """ コード上の文字を書き換える。

        Params:
            row = 行。
            col = 列。
            character = 書き換える文字。

        Throws:
            RuntimeError 位置がコード外だった場合。
        """

        assert row >= 0
        assert col >= 0
        assert len(character) == 1

        if row >= len(self.__code) or col >= len(self.__code[row]):
            raise RuntimeError("The index was out of bounds.")

        before = self.__code[row][:col]
        after = self.__code[row][col + 1:]

        self.__code[row] = before + character + after

    def __check_code(self) -> None:
        """ コードの形が正しいか調べる。

        Throws:
            RuntimeError コードの形が正しくない場合。
        """

        if len(self.__code) == 0:
            raise RuntimeError("The code has no lines.")

        lines_head = len(self.__code[0])

        for line in self.__code[1:]:
            if len(line) != lines_head:
                raise RuntimeError("The code wasn't rectangular.")

    def __move(self) -> None:
        """ コード上を移動する。
        """

        row = self.__row + self.__row_movement
        col = self.__col + self.__col_movement

        self.__row = circulate(row, 0, self.__rows - 1)
        self.__col = circulate(col, 0, self.__cols - 1)


def circulate(number: int, lower: int, upper: int) -> int:
    """ 数を範囲内で循環させる。

    Params:
        number = 数。
        lower = 数の下限。
        upper = 数の上限。

    Returns: 循環させた数。
    """

    if lower <= number <= upper:
        return number

    elif number < lower:
        return circulate(upper + lower + number + 1, lower, upper)

    else:
        return circulate(lower + number - upper - 1, lower, upper)
