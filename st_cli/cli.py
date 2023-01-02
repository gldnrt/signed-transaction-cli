from .params import get_params
from .transaction import Transaction




def get_params_file_path(argv: list[str]) -> str:
    """実行コマンドの第1引数に指定されたファイルパスを返す"""

    if 2 != len(argv):
        raise ReferenceError("Usage: st_cli [FILE_PATH]")

    return argv[1]


def create_signed_transaction(argv: list[str]) -> None:
    """オフラインで署名済み送金用トランザクションを作成する"""

    params_file_path = get_params_file_path(argv)
    params = get_params(params_file_path)

    myTransaction = Transaction(params)
    signed_tx = myTransaction.create_signed_tx()
    print(signed_tx)
