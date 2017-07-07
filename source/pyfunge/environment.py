""" 環境モジュール。

Date: 2017/7/7
Authors: masaniwa
"""

from pyfunge.codestream import CodeStream


class Environment:
    """ 環境。
    """

    def __init__(self, code):
        """ 初期化する。

        Params:
            code = Befungeのコード。
        """

        self.__stack = Stack()
        self.__quoting = False
        self.__code = CodeStream(code)
        self.__input = Queue()

    def get_stack(self):
        """ スタックを得る。

        Returns: スタック。
        """

        return self.__stack

    def get_quoting(self):
        """ コードの文字を命令とするかスタックへのプッシュとするかどうかを得る。

        Returns: 命令とする場合はTrue。スタックへのプッシュとする場合はFalse。
        """

        return self.__quoting

    def set_quoting(self, value):
        """ コードの文字を命令とするかスタックへのプッシュとするかどうか設定する。

        Params:
            value = 命令とする場合はTrue。スタックへのプッシュとする場合はFalse。
        """

        self.__quoting = value

    def get_code(self):
        """ コードを得る。

        Returns: コード。
        """

        return self.__code

    def get_input(self):
        """ 入力データのキューを得る。

        Returns: 入力データのキュー。
        """

        return self.__input


class Stack:
    """ スタック。
    """

    def __init__(self):
        self.__data = []

    def __len__(self):
        return len(self.__data)

    def push(self, element):
        """ スタックへ値をプッシュする。

        Params:
            element = プッシュする値。
        """

        self.__data.append(element)

    def pop(self):
        """ スタックから値をポップする。

        Returns: ポップした値。
        """

        return self.__data.pop()


class Queue:
    """ キュー。
    """

    def __init__(self):
        self.__data = []

    def __len__(self):
        return len(self.__data)

    def enqueue(self, element):
        """ キューへ値を追加する。

        Params:
            element = 追加する値。
        """

        self.__data.append(element)

    def dequeue(self):
        """ キューから値を取り出す。

        Returns: 取り出した値。
        """

        return self.__data.pop(0)
