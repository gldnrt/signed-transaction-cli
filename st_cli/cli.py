import os
import json
from jsonschema import validate, ValidationError
from .transaction import Transaction


def check_params(params: object) -> None:
    '''入力paramがスキーマに即しているかを確認する'''

    parentdir = os.path.dirname(__file__)
    schema_file_path = parentdir + '/schema.json'

    with open(schema_file_path) as file_obj:
        json_schema = json.load(file_obj)

    try:
        validate(params, json_schema)
    except ValidationError as e:
        raise RuntimeError("Error: ignore params file, " + e.message)

    return


def get_params(argv: list[str]) -> object:
    """第1引数に指定されたjsonパラメータファイルを読み込む"""

    if 2 != len(argv):
        raise ReferenceError("Usage: st_cli [FILE_PATH]")

    try:
        with open(argv[1]) as f:
            params = json.load(f)
    except Exception as e:
        raise ReferenceError("Error: ignore params file, " + str(e))

    return params


def create_signed_transaction(argv: list[str]) -> None:
    """オフラインで署名済み送金用トランザクションを作成する"""

    params = get_params(argv)
    check_params(params)

    myTransaction = Transaction(params)
    signed_tx = myTransaction.create_signed_tx()
    print(signed_tx)
