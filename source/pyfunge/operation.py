""" 命令モジュール。

2017/4/16 masaniwa
"""

from abc import ABC
from random import randrange

from .codestream import Direction


class Operator(ABC):
    """ 命令の基底クラス。
    """

    def apply(self, environment):
        """ 環境に対して命令を実行する。
        """

        pass


class Director(Operator):
    """ 方向を変える命令。
    """

    def __init__(self, direction):
        self.__direction = direction

    def apply(self, environment):
        environment.get_code().change_direction(self.__direction)


class Selector(Operator):
    """ スタックをポップして0なら方向Aへ、違うなら方向Bへ転換する命令。
    """

    def __init__(self, direction_a, direction_b):
        self.__direction_a = direction_a
        self.__direction_b = direction_b

    def apply(self, environment):
        if environment.get_stack().pop() == 0:
            environment.get_code().change_direction(self.__direction_a)

        else:
            environment.get_code().change_direction(self.__direction_b)


class Random(Operator):
    """ ランダムに方向を変える命令。
    """

    def apply(self, environment):
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

    def apply(self, environment):
        return


class Skipper(Operator):
    """ 次の命令を飛ばす命令。
    """

    def apply(self, environment):
        environment.get_code().skip()


class Stopper(Operator):
    """ プログラムを終了する命令。
    """

    def apply(self, environment):
        environment.get_code().stop()


class Quoter(Operator):
    """ 文字を命令とするかスタックへのプッシュとするかを切り替える命令。
    """

    def apply(self, environment):
        environment.set_quoting(not environment.get_quoting())


class Value(Operator):
    """ スタックへ値をプッシュする命令。
    """

    def __init__(self, value):
        self.__value = value

    def apply(self, environment):
        environment.get_stack().push(self.__value)


class NumberInput(Operator):
    """ 数値を入力させてスタックへプッシュする命令。
    """

    def apply(self, environment):
        while True:
            character = input(">")

            if character.isdigit():
                environment.get_stack().push(int(character))

                break


class CharInput(Operator):
    """ 文字を入力させてそのASCIIコードをスタックへプッシュする命令。
    """

    def apply(self, environment):
        while True:
            character = input(">")

            if len(character) > 0:
                environment.get_stack().push(ord(character[0]))

                break


class NumberPrinter(Operator):
    """ スタックをポップして値を表示する命令。
    """

    def apply(self, environment):
        print(environment.get_stack().pop(), " ", end="")


class CharPrinter(Operator):
    """ スタックをポップしてASCIIコードの文字を表示する命令。
    """

    def apply(self, environment):
        print(chr(environment.get_stack().pop()), end="")


class Calculater(Operator):
    """ スタックからy, xをポップしてx, yを引数に関数を実行してプッシュする命令。
    """

    def __init__(self, function):
        self.__function = function

    def apply(self, environment):
        y = environment.get_stack().pop()
        x = environment.get_stack().pop()

        environment.get_stack().push(self.__function(x, y))


class Inverter(Operator):
    """ スタックからポップして0なら1、そうでないなら0をプッシュする命令。
    """

    def apply(self, environment):
        value = 1 if environment.get_stack().pop() == 0 else 0

        environment.get_stack().push(value)


class Duplicator(Operator):
    """ スタックからポップして2度プッシュする命令。
    """

    def apply(self, environment):
        value = environment.get_stack().pop()

        environment.get_stack().push(value)
        environment.get_stack().push(value)


class Reverser(Operator):
    """ スタックからy, xをポップしてx, yをプッシュする命令。
    """

    def apply(self, environment):
        y = environment.get_stack().pop()
        x = environment.get_stack().pop()

        environment.get_stack().push(y)
        environment.get_stack().push(x)


class Popper(Operator):
    """ スタックからポップして値を捨てる命令。
    """

    def apply(self, environment):
        environment.get_stack().pop()


class Reader(Operator):
    """ スタックから行、列をポップしてコードの該当位置のASCIIコードをプッシュする命令。
    """

    def apply(self, environment):
        row = environment.get_stack().pop()
        col = environment.get_stack().pop()

        value = ord(environment.get_code().read_char(row, col))

        environment.get_stack().push(value)


class Writer(Operator):
    """ スタックから行、列、ASCIIコードをポップしてコードの該当位置をASCIIコードの文字にする命令。
    """

    def apply(self, environment):
        row = environment.get_stack().pop()
        col = environment.get_stack().pop()
        val = environment.get_stack().pop()

        environment.get_code().write_char(row, col, chr(val))
