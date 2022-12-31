import subprocess
import json


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

        try:
            result = subprocess.run(
                command,
                shell=True,  # TODO: インジェクション攻撃防止のためfalseにする
                capture_output=True,
                text=True,
                check=True,
            )
        except Exception:
            # TODO: 引数にerr_messageを追加し、以下のメッセージに表示する
            raise RuntimeError("Error, command execution failed, " + command)

        return result.stdout

    def __run_shell_command_json(self, command) -> str:
        """コマンドを実行し、標準出力結果をjson形式で返す"""

        result = self.__run_shell_command(command)
        return json.loads(result)

    def create_raw_tx(self) -> str:
        """送金用のRaw Transactionを作成する"""

        inputs = [self.params["unspent_tx"]]
        outputs = {self.params["dest_address"]: self.params["amount"]}

        cmd_createrawtransaction = (
            "bitcoin-cli "
            + self.network_arg
            + " createrawtransaction '"
            + json.dumps(inputs)
            + "' '"
            + json.dumps(outputs)
            + "'"
        )

        raw_tx = self.__run_shell_command(cmd_createrawtransaction)
        raw_tx = raw_tx.replace("\n", "")

        return raw_tx

    def sign_raw_tx_with_wallet(self, raw_tx) -> object:
        """
        walletを使用してRaw Transactionに署名する
        前提としてwalletがloadされていること
        """

        cmd = (
            "bitcoin-cli "
            + self.network_arg
            + " signrawtransactionwithwallet "
            + raw_tx
        )
        signed_result = self.__run_shell_command_json(cmd)
        if signed_result["complete"] is not True:
            raise RuntimeError("Error, sign raw_tx failed")

        return signed_result["hex"]

    def create_signed_tx(self) -> str:
        """オフラインで使用可能な署名済みトランザクションを作成する"""

        raw_tx = self.create_raw_tx()
        signed_tx = self.sign_raw_tx_with_wallet(raw_tx)

        return signed_tx
