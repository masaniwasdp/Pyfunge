""" パーサモジュール。

Date: 2017/7/13
Authors: masaniwa
"""

from pyfunge import operation
from pyfunge.codestream import Direction
from pyfunge.operation import Operator


def parse(character: str, quoting: bool) -> Operator:
    """ 文字を命令にパースする。

    Params:
        character = パース対象の文字。
        quoting = 文字を文字とする場合はTrue。文字を命令とする場合はFalse。

    Returns: パースした命令。

    Throws:
        RuntimeError 文字をパースできなかった場合。
    """

    assert len(character) == 1

    if character == "\"":
        return operation.Quoter()

    if quoting:
        return operation.Value(ord(character))

    if character.isdigit():
        return operation.Value(int(character))

    if character not in operations:
        raise RuntimeError("The character isn't an operator.")

    return operations[character]


operations = {
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
