""" 環境モジュール。

2017/4/16 masaniwa
"""

from .codestream import CodeStream


class Environment:
    """ 環境。
    """

    def __init__(self, code):
        self.__stack = Stack()
        self.__quoting = False
        self.__code = CodeStream(code)
        self.__input = Queue()

    def get_stack(self):
        """ スタックを返す。
        """

        return self.__stack

    def get_quoting(self):
        """ コードの文字を命令とするかスタックへのプッシュとするかどうかを返す。
        """

        return self.__quoting

    def set_quoting(self, value):
        """ コードの文字を命令とするかスタックへのプッシュとするかどうかを設定する。
        """

        self.__quoting = value

    def get_code(self):
        """ コードを返す。
        """

        return self.__code

    def get_input(self):
        """ 入力データのキューを返す。
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
        """

        self.__data.append(element)

    def pop(self):
        """ スタックから値をポップして返す。
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
        """

        self.__data.append(element)

    def dequeue(self):
        """ キューから値を取り出して返す。
        """

        return self.__data.pop(0)
