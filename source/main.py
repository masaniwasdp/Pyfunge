""" メインエントリ。

Date: 2017/7/15
Authors: masaniwa
"""

from sys import argv

from pyfunge.app import App

usage = "Usage: [path]"


def main():
    if len(argv) < 2:
        print(usage)

        return

    try:
        App(argv[1]).run()

    except KeyboardInterrupt:
        print()

    except OSError as e:
        print(e.args[1])

    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
