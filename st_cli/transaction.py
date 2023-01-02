import subprocess
import json
import sys


class Transaction:
    """トランザクションを扱うクラス"""

    params = None
    network_arg = "-unspecified-network"

    def __init__(self, params: object) -> None:
        """params: 入力パラメータ"""

        self.params = params
        self.network_arg = "-" + params["network"]

    def __run_shell_command(self, command_elements: list[str]) -> str:
        """コマンドを実行し、標準出力結果を返す"""

        result = subprocess.run(
            command_elements,
            capture_output=True,
            text=True,
        )

        if 0 != result.returncode:
            sys.stderr.write(result.stderr)
            raise RuntimeError(
                "Error, command failed, " + " ".join(command_elements)
                )

        return result.stdout

    def __run_shell_command_json(self, command_elements: list[str]) -> str:
        """コマンドを実行し、標準出力結果をjson形式で返す"""

        result = self.__run_shell_command(command_elements)
        return json.loads(result)

    def __modify_float_notation_for_json(
            self, num: float, digits: int = 8
            ) -> float:
        '''
        json dump後の小数点以下の浮動小数点表記を、指定桁に丸める
        - 浮動小数点をjson dumpすると、誤差により小数点の桁数が大きくなる問題の修正
        ex) digits=8のとき、12.12345678999 -> 12.12345679(y:8桁)
        '''
        modified_num = json.loads(
            json.dumps(num),
            parse_float=lambda x: round(float(x), digits)
        )

        return modified_num

    def create_raw_tx(self) -> str:
        """送金用の未署名Raw Transactionを作成する"""

        tx_inputs = [
            {
                "txid": self.params["specified_utxo"]["txid"],
                "vout": self.params["specified_utxo"]["vout"]
            }
        ]

        remittance_amount = self.params["remittance_amount"]
        charge = self.params["specified_utxo"]["amount"] \
            - remittance_amount - self.params["transaction_fee"]
        charge = self.__modify_float_notation_for_json(charge)

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

    def sign_raw_tx_with_wallet(self, raw_tx: str) -> str:
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
