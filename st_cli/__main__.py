import sys
from . import cli


def main():
    """cli.create_signed_transactionの実行およびエラー処理"""

    try:
        cli.create_signed_transaction(sys.argv)
    except Exception as e:
        print(e, file=sys.stderr)
        exit(1)


if __name__ == "__main__":
    main()
