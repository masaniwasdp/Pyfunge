""" アプリケーションモジュール。

Date: 2017/7/7
Authors: masaniwa
"""

from pyfunge.environment import Environment
from pyfunge.parser import Parser


class App:
    """ アプリケーション。
    """

    def __init__(self, path):
        with open(path, "r") as code:
            self.__environment = Environment(code.read())

    def run(self):
        """ アプリケーションを実行する。
        """

        for character in self.__environment.get_code():
            quoting = self.__environment.get_quoting()

            operator = Parser.parse(character, quoting)

            operator.apply(self.__environment)

        print()
