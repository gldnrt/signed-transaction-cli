import json


def get_params(argv):
    """第1引数に指定されたjsonパラメータファイルを読み込む"""

    if len(argv) != 2:
        raise ReferenceError("Usage: st_cli [FILE_PATH]")

    try:
        with open(argv[1]) as f:
            params = json.load(f)
    except Exception:
        raise ReferenceError("Error: ignore params file, " + argv[1])

    return params


def create_signed_transaction(argv):
    # TODO: オフラインで署名済み送金用トランザクションを作成する

    params = get_params(argv)
    print(params)
