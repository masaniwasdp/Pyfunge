""" メインエントリ。

Date: 2017/7/7
Authors: masaniwa
"""

from sys import argv

from pyfunge.app import App


def __main():
    if len(argv) > 1:
        App(argv[1]).run()


if __name__ == "__main__":
    __main()
