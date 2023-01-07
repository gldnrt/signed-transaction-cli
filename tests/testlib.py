import json
import subprocess
import os


def run_command(command) -> str:
    '''シェルコマンド実行後、標準出力を返す'''

    proc = subprocess.run(
        command, shell=True, capture_output=True, text=True, check=True
    )

    return proc.stdout


def run_command_json(command) -> dict:
    '''シェルコマンド実行後、標準出力をdictに変換して返す'''

    result = run_command(command)
    return json.loads(result)


def create_default_params() -> dict:
    '''
    デフォルトの試験用入力パラメータを作成
    前提: listunspent[0]に十分な(fee以上の)amountがあること
    '''

    cmd = 'bitcoin-cli -regtest getnewaddress "Dest Address"'
    dest_address = run_command(cmd)
    dest_address = dest_address.replace("\n", "")

    cmd = 'bitcoin-cli -regtest getnewaddress "Sender Charge Address"'
    sender_charge_address = run_command(cmd)
    sender_charge_address = sender_charge_address.replace("\n", "")

    listunspent = run_command_json(
        "bitcoin-cli -regtest listunspent"
        )

    target_utx = listunspent[0]
    remittance_amount = target_utx["amount"]/4

    params = {
        "network": "regtest",
        "remittance_amount": remittance_amount,
        "transaction_fee": 0.00001,
        "specified_utxo": {
            "txid": target_utx["txid"],
            "vout": target_utx["vout"],
            "amount": target_utx["amount"]
            },
        "address": {
            "destination": dest_address,
            "sender_charge": sender_charge_address
        }
    }

    # jsonの浮動小数点表記を小数点以下8桁に丸める
    params = json.loads(
        json.dumps(params),
        parse_float=lambda x: round(float(x), 8))

    return params


def get_default_input_file_path():
    '''デフォルトの入力ファイルのパスを返す'''
    input_file_path = "./tests/test_params/auto_created_test_params.json"
    
    return input_file_path


def create_input_file(params: dict, path: str = get_default_input_file_path()):
    '''paramsをファイル出力する'''

    with open(path, "w") as fout:
        json.dump(params, fout, indent=2)

    os.sync()


def delete_input_file(path: str = get_default_input_file_path()):
    '''pathのファイルを削除する'''
    os.remove(path)
    os.sync()
