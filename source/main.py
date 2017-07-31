""" メインエントリ。

Date: 2017/7/31
Authors: masaniwa
"""

from sys import argv

from pyfunge.app import App

USAGE = "Usage: [path]"


def main():
    if len(argv) < 2:
        print(USAGE)

        return

    try:
        App(argv[1]).run()

    except KeyboardInterrupt:
        print()

    except OSError as e:
        print(e.args[1])

    except RuntimeError as e:
        print(e)


if __name__ == "__main__":
    main()
