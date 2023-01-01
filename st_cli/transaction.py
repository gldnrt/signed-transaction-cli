import subprocess
import json
import sys


class Transaction:
    """トランザクションを扱うクラス"""

    params = None
    network_arg = "-unspecified-network"

    def __init__(self, params) -> None:
        """params: 入力パラメータ"""
        self.params = params

        # インジェクション攻撃防止のため判定処理をする
        if "regtest" == params["network"]:
            self.network_arg = "-regtest"
        elif "testnet" == params["network"]:
            self.network_arg = "-testnet"
        elif "mainnet" == params["network"]:
            # 動作確認対象外
            self.network_arg = "-mainnet"
        else:
            raise RuntimeError('Error: "network" parameter is invalid')

    def __run_shell_command(self, command) -> str:
        """コマンドを実行し、標準出力結果を返す"""
        result = subprocess.run(
            command,
            shell=False,
            capture_output=True,
            text=True,
        )
        
        if 0 != result.returncode:
            sys.stderr.write(result.stderr)
            raise RuntimeError("Error, command failed, " + " ".join(command))

        return result.stdout

    def __run_shell_command_json(self, command) -> str:
        """コマンドを実行し、標準出力結果をjson形式で返す"""

        result = self.__run_shell_command(command)
        return json.loads(result)

    def create_raw_tx(self) -> str:
        """送金用のRaw Transactionを作成する"""

        tx_inputs = [
            {
                "txid": self.params["unspent_transaction"]["txid"],
                "vout": self.params["unspent_transaction"]["vout"]
            }
        ]

        remittance_amount = self.params["remittance_amount"]
        charge = self.params["unspent_transaction"]["value"] \
            - remittance_amount - self.params["transaction_fee"]
        # 小数点以下8桁に丸める
        charge = json.loads(
            json.dumps(charge),
            parse_float=lambda x: round(float(x), 8))

        tx_outputs = {
            self.params["address"]["destination"]: remittance_amount,
            self.params["address"]["sender_charge"]: charge
        }

        cmd_createrawtransaction = [
            "bitcoin-cli",
            self.network_arg,
            "createrawtransaction",
            json.dumps(tx_inputs),
            json.dumps(tx_outputs)
        ]

        raw_tx = self.__run_shell_command(cmd_createrawtransaction)
        raw_tx = raw_tx.replace("\n", "")

        return raw_tx

    def sign_raw_tx_with_wallet(self, raw_tx) -> object:
        """
        walletを使用してRaw Transactionに署名する
        前提としてwalletがloadされていること
        """

        signe_cmd = [
            "bitcoin-cli",
            self.network_arg,
            "signrawtransactionwithwallet",
            raw_tx
            ]
                
        signed_result = self.__run_shell_command_json(signe_cmd)
        if signed_result["complete"] is not True:
            raise RuntimeError("Error, sign raw_tx failed")

        return signed_result["hex"]

    def create_signed_tx(self) -> str:
        """オフラインで使用可能な署名済みトランザクションを作成する"""

        raw_tx = self.create_raw_tx()
        signed_tx = self.sign_raw_tx_with_wallet(raw_tx)

        return signed_tx
