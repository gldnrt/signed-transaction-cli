import os
import json
from jsonschema import validate, ValidationError


def check_params(params: dict) -> None:
    '''入力paramがスキーマに即しているかを確認する'''

    parentdir = os.path.dirname(__file__)
    schema_file_path = parentdir + "/schema.json"

    with open(schema_file_path) as file_obj:
        json_schema = json.load(file_obj)

    try:
        validate(params, json_schema)
    except ValidationError as e:
        raise RuntimeError("Error: ignore params file, " + e.message)

    return


def read_params_from_file(param_file_path: str) -> dict:
    """パラメータファイルを読み込み、jsonからdictに変換する"""

    try:
        with open(param_file_path) as f:
            params = json.load(f)
    except Exception as e:
        raise ReferenceError("Error: ignore params file, " + str(e))

    return params


def get_params(param_file_path: str) -> dict:
    '''指定されたファイルからパラメータを取得する'''

    params = read_params_from_file(param_file_path)
    check_params(params)

    return params
