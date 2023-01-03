import sys
from . import cli


def main() -> None:
    """cli.main()を呼び出す"""

    cli.cli_main(sys.argv)


if __name__ == "__main__":
    main()
