""" パーサモジュール。

2017/4/16 masaniwa
"""

from .codestream import Direction

from . import operation


class Parser:
    """ パーサ。
    """

    __operations = {
            "<": operation.Director(Direction.left),
            ">": operation.Director(Direction.right),
            "^": operation.Director(Direction.up),
            "v": operation.Director(Direction.down),
            "_": operation.Selector(Direction.right, Direction.left),
            "|": operation.Selector(Direction.down, Direction.up),
            "?": operation.Random(),
            " ": operation.Space(),
            "#": operation.Skipper(),
            "@": operation.Stopper(),
            "&": operation.NumberInput(),
            "~": operation.CharInput(),
            ".": operation.NumberPrinter(),
            ",": operation.CharPrinter(),
            "+": operation.Calculater(lambda x, y: x + y),
            "-": operation.Calculater(lambda x, y: x - y),
            "*": operation.Calculater(lambda x, y: x * y),
            "/": operation.Calculater(lambda x, y: x // y),
            "%": operation.Calculater(lambda x, y: x % y),
            "`": operation.Calculater(lambda x, y: 1 if x > y else 0),
            "!": operation.Inverter(),
            ":": operation.Duplicator(),
            "\\": operation.Reverser(),
            "$": operation.Popper(),
            "g": operation.Reader(),
            "p": operation.Writer()}

    @classmethod
    def parse(cls, character, quoting):
        """ 文字を命令にパースして返す。
        """

        if character == "\"":
            return operation.Quoter()

        if quoting:
            return operation.Value(ord(character))

        if character.isdigit():
            return operation.Value(int(character))

        return cls.__operations[character]
