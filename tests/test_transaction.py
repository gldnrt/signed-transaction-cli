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
        vout = listunspent[0]["vout"]
        txid = listunspent[0]["txid"]
        amount = listunspent[0]["amount"] - 0.0001

        cmd = 'bitcoin-cli -regtest getnewaddress "Dest Address"'
        dest_address = self.run_command(cmd)
        dest_address = dest_address.replace("\n", "")

        params = {
            "network": "regtest",
            "unspent_tx": {"txid": txid, "vout": vout},
            "amount": amount,
            "dest_address": dest_address,
        }

        # 実行
        myTransaction = Transaction(params)
        signed_tx = myTransaction.create_signed_tx()

        # ブロードキャストして確認 - 失敗時は例外がスローされる
        cmd = "bitcoin-cli -regtest sendrawtransaction " + signed_tx
        self.run_command(cmd)
