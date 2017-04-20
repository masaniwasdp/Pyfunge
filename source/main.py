""" メインエントリ。

2017/4/16 masaniwa
"""

from sys import argv

from pyfunge.app import App


def __main():
    if len(argv) < 2:
        return

    App(argv[1]).run()


if __name__ == "__main__":
    __main()
