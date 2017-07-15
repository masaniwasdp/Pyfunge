""" アプリケーションモジュール。

Date: 2017/7/14
Authors: masaniwa
"""

from pyfunge.environment import Environment
from pyfunge.parser import parse


class App:
    """ アプリケーション。
    """

    def __init__(self, path: str) -> None:
        """ 初期化する。

        Params:
            path = Befungeのコードのパス。

        Throws:
            OSError コード読み込みに失敗した場合。
            RuntimeError コードが正しい形でない場合。
        """

        with open(path, "r") as code:
            self.__environment = Environment(code.read())

    def run(self) -> None:
        """ アプリケーションを実行する。

        Throws:
            RuntimeError エラーが発生した場合。
        """

        for character in self.__environment.get_code():
            quoting = self.__environment.get_quoting()

            operator = parse(character, quoting)

            operator.apply(self.__environment)

        print()
