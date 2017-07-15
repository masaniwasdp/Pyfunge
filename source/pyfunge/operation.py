""" 命令モジュール。

Date: 2017/7/14
Authors: masaniwa
"""

from typing import Callable
from random import randrange

from pyfunge.codestream import Direction
from pyfunge.environment import Environment


class Operator:
    """ 命令の基底クラス。
    """

    def apply(self, environment: Environment) -> None:
        """ 環境に対して命令を実行する。

        Params:
            environment = 環境。

        Throws:
            RuntimeError 実行時エラーが発生した場合。
        """

        pass


class Director(Operator):
    """ 方向を変える命令。
    """

    def __init__(self, direction: Direction) -> None:
        """ 初期化する。

        Params:
            direction = 方向。
        """

        self.__direction = direction

    def apply(self, environment: Environment) -> None:
        environment.get_code().change_direction(self.__direction)


class Selector(Operator):
    """ スタックをポップして0なら方向Aへ、違うなら方向Bへ転換する命令。
    """

    def __init__(self, direction_a: Direction, direction_b: Direction) -> None:
        """ 初期化する。

        Params:
            direction_a = 方向A。
            direction_b = 方向B。
        """

        self.__direction_a = direction_a
        self.__direction_b = direction_b

    def apply(self, environment: Environment) -> None:
        if environment.get_stack().pop() == 0:
            environment.get_code().change_direction(self.__direction_a)

        else:
            environment.get_code().change_direction(self.__direction_b)


class Random(Operator):
    """ ランダムに方向を変える命令。
    """

    def apply(self, environment: Environment) -> None:
        random = randrange(4)

        if random == 0:
            environment.get_code().change_direction(Direction.right)

        elif random == 1:
            environment.get_code().change_direction(Direction.left)

        elif random == 2:
            environment.get_code().change_direction(Direction.up)

        else:
            environment.get_code().change_direction(Direction.down)


class Space(Operator):
    """ 何もしない命令。
    """

    def apply(self, environment: Environment) -> None:
        return


class Skipper(Operator):
    """ 次の命令を飛ばす命令。
    """

    def apply(self, environment: Environment) -> None:
        environment.get_code().skip()


class Stopper(Operator):
    """ プログラムを終了する命令。
    """

    def apply(self, environment: Environment) -> None:
        environment.get_code().stop()


class Quoter(Operator):
    """ 文字を命令とするかスタックへのプッシュとするかを切り替える命令。
    """

    def apply(self, environment: Environment) -> None:
        environment.set_quoting(not environment.get_quoting())


class Value(Operator):
    """ スタックへ値をプッシュする命令。
    """

    def __init__(self, value: int) -> None:
        """ 初期化する。

        Params:
            value = 値。
        """

        self.__value = value

    def apply(self, environment: Environment) -> None:
        environment.get_stack().push(self.__value)


class NumberInput(Operator):
    """ 入力された数値ひとつをスタックへプッシュする命令。
    """

    def apply(self, environment: Environment) -> None:
        while True:
            try:
                element = get_input_element(environment)

                if element.isdigit():
                    environment.get_stack().push(int(element))

                    break

            except EOFError as e:
                raise RuntimeError("Failed to read input.") from e


class CharInput(Operator):
    """ 入力された文字ひとつのASCIIコードをスタックへプッシュする命令。
    """

    def apply(self, environment: Environment) -> None:
        try:
            element = get_input_element(environment)

            environment.get_stack().push(ord(element))

        except EOFError as e:
            raise RuntimeError("Failed to read input.") from e


class NumberPrinter(Operator):
    """ スタックをポップして値を表示する命令。
    """

    def apply(self, environment: Environment) -> None:
        print(environment.get_stack().pop(), " ", end="")


class CharPrinter(Operator):
    """ スタックをポップしてASCIIコードの文字を表示する命令。
    """

    def apply(self, environment: Environment) -> None:
        print(chr(environment.get_stack().pop()), end="")


class Calculater(Operator):
    """ スタックからy, xをポップしてx, yを引数に関数を実行してプッシュする命令。
    """

    def __init__(self, function: Callable[[int, int], int]) -> None:
        """ 初期化する。

        Params:
            function = 関数。
        """

        self.__function = function

    def apply(self, environment: Environment) -> None:
        y = environment.get_stack().pop()
        x = environment.get_stack().pop()

        environment.get_stack().push(self.__function(x, y))


class Inverter(Operator):
    """ スタックからポップして0なら1、そうでないなら0をプッシュする命令。
    """

    def apply(self, environment: Environment) -> None:
        value = 1 if environment.get_stack().pop() == 0 else 0

        environment.get_stack().push(value)


class Duplicator(Operator):
    """ スタックからポップして2度プッシュする命令。
    """

    def apply(self, environment: Environment) -> None:
        value = environment.get_stack().pop()

        environment.get_stack().push(value)
        environment.get_stack().push(value)


class Reverser(Operator):
    """ スタックからy, xをポップしてx, yをプッシュする命令。
    """

    def apply(self, environment: Environment) -> None:
        y = environment.get_stack().pop()
        x = environment.get_stack().pop()

        environment.get_stack().push(y)
        environment.get_stack().push(x)


class Popper(Operator):
    """ スタックからポップして値を捨てる命令。
    """

    def apply(self, environment: Environment) -> None:
        environment.get_stack().pop()


class Reader(Operator):
    """ スタックから行、列をポップしてコードの該当位置のASCIIコードをプッシュする命令。
    """

    def apply(self, environment: Environment) -> None:
        row = environment.get_stack().pop()
        col = environment.get_stack().pop()

        value = ord(environment.get_code().read_char(row, col))

        environment.get_stack().push(value)


class Writer(Operator):
    """ スタックから行、列、ASCIIコードをポップしてコードの該当位置をASCIIコードの文字にする命令。
    """

    def apply(self, environment: Environment) -> None:
        row = environment.get_stack().pop()
        col = environment.get_stack().pop()
        val = environment.get_stack().pop()

        environment.get_code().write_char(row, col, chr(val))


def get_input_element(environment: Environment) -> str:
    """ 入力データのキューからひとつ取り出す。

    キューが空なら入力を受け付けてキューに追加する。

    Params:
        environment = 環境。

    Returns: 取り出した値。

    Throws:
        EOFError 入力を取得できなかった場合。
    """

    while True:
        if len(environment.get_input()) > 0:
            return environment.get_input().dequeue()

        else:
            for element in input("\npyfunge > "):
                environment.get_input().enqueue(element)
