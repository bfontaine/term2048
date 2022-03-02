import sys
from ptyprocess import PtyProcessUnicode


def main():
    """
    Run 'poetry run python tests/test.py' in a pseudo terminal.
    """
    p = PtyProcessUnicode.spawn(['poetry', 'run', 'python', 'tests/test.py'])

    while True:
        try:
            sys.stdout.write(p.read())
        except EOFError:
            break

    p.wait()


if __name__ == '__main__':
    main()
