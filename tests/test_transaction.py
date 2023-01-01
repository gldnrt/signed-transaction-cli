import subprocess
import json
from st_cli.transaction import Transaction


class TestTransaction:
    # TODO: 個別メソッドの単体テスト作成

    def run_command(self, command):
        return subprocess.run(
            command, shell=True, capture_output=True, text=True, check=True
        ).stdout

    def run_command_json(self, command):
        result = self.run_command(command)
        return json.loads(result)

    def test_create_signed_tx(self):
        # 送金用コイン作成
        cmd = (
            "bitcoin-cli -regtest generatetoaddress 101 "
            + '$(bitcoin-cli -regtest getnewaddress "sender")'
        )
        self.run_command(cmd)

        # 入力パラメータparams作成
        listunspent = self.run_command_json("bitcoin-cli -regtest listunspent")

        cmd = 'bitcoin-cli -regtest getnewaddress "Dest Address"'
        dest_address = self.run_command(cmd)
        dest_address = dest_address.replace("\n", "")

        cmd = 'bitcoin-cli -regtest getnewaddress "Sender Charge Address"'
        sender_charge_address = self.run_command(cmd)
        sender_charge_address = sender_charge_address.replace("\n", "")

        remittance_amount = listunspent[0]["amount"]/4

        params = {
            "network": "regtest",
            "remittance_amount": remittance_amount,
            "transaction_fee": 0.00001,
            "unspent_transaction": {
                "txid": listunspent[0]["txid"],
                "vout": listunspent[0]["vout"],
                "value": listunspent[0]["amount"]
                },
            "address": {
                "destination": dest_address,
                "sender_charge": sender_charge_address
            }
        }

        # 浮動小数点を小数点以下8桁に丸める
        params = json.loads(
            json.dumps(params),
            parse_float=lambda x: round(float(x), 8))

        # 実行
        myTransaction = Transaction(params)
        signed_tx = myTransaction.create_signed_tx()

        # ブロードキャストして確認 - 失敗時は例外がスローされてテスト失敗
        cmd = "bitcoin-cli -regtest sendrawtransaction " + signed_tx
        self.run_command(cmd)
