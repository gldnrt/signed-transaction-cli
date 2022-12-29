import sys
from . import cli


def main():
    try:
        cli.create_signed_transaction(sys.argv)
    except Exception as e:
        print(e, file=sys.stderr)
        exit(1)


if __name__ == "__main__":
    main()
