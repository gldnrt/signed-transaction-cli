import subprocess
import json
import pytest
import re
from st_cli.transaction import Transaction


class TestTransaction:
    '''
    Transactionテストクラス
    前提: walletがロードされていること
    '''

    @classmethod
    def __run_command(self, command) -> str:
        '''シェルコマンド実行後、標準出力を返す'''

        proc = subprocess.run(
            command, shell=True, capture_output=True, text=True, check=True
        )

        return proc.stdout

    def __run_command_json(self, command) -> object:
        '''シェルコマンド実行後、標準出力をjsonに変換して返す'''

        result = self.__run_command(command)
        return json.loads(result)

    def __create_default_params(self) -> object:
        '''
        デフォルトの試験用入力パラメータを作成
        '''

        cmd = 'bitcoin-cli -regtest getnewaddress "Dest Address"'
        dest_address = self.__run_command(cmd)
        dest_address = dest_address.replace("\n", "")

        cmd = 'bitcoin-cli -regtest getnewaddress "Sender Charge Address"'
        sender_charge_address = self.__run_command(cmd)
        sender_charge_address = sender_charge_address.replace("\n", "")

        listunspent = self.__run_command_json(
            "bitcoin-cli -regtest listunspent"
            )

        target_utx = listunspent[-1]
        remittance_amount = target_utx["amount"]/4

        params = {
            "network": "regtest",
            "remittance_amount": remittance_amount,
            "transaction_fee": 0.00001,
            "unspent_transaction": {
                "txid": target_utx["txid"],
                "vout": target_utx["vout"],
                "value": target_utx["amount"]
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

    def setup_class(cls):
        # 送金用コイン生成
        cmd = (
            "bitcoin-cli -regtest generatetoaddress 101 "
            + '$(bitcoin-cli -regtest getnewaddress "sender")'
        )
        cls.__run_command(cmd)

    def test_constructor_regtest(self):
        params = {"network": "regtest"}

        myTx = Transaction(params)

        assert myTx.params == params
        assert myTx.network_arg == "-regtest"

    def test_constructor_testnet(self):
        params = {"network": "testnet"}

        myTx = Transaction(params)

        assert myTx.params == params
        assert myTx.network_arg == "-testnet"

    def test_constructor_mainnet(self):
        params = {"network": "mainnet"}

        myTx = Transaction(params)

        assert myTx.params == params
        assert myTx.network_arg == "-mainnet"

    def test_constructor_ignore_network(self):
        params = {"network": "ignore"}

        with pytest.raises(RuntimeError) as e:
            Transaction(params)

        assert str(e.value) == 'Error: "network" parameter is invalid, ignore'

    def test_create_raw_tx(self):
        params = self.__create_default_params()
        myTx = Transaction(params)

        raw_tx = myTx.create_raw_tx()

        assert re.match(r"^[0-9a-f]+$", raw_tx)
        
    def test_create_raw_tx_ignore_param(self):
        params = self.__create_default_params()
        params['unspent_transaction']['txid'] = 'ignore_txid'
        myTx = Transaction(params)

        with pytest.raises(RuntimeError):
            myTx.create_raw_tx()

    def test_sign_raw_tx_with_wallet(self):
        params = self.__create_default_params()
        myTx = Transaction(params)
        raw_tx = myTx.create_raw_tx()

        signed_tx = myTx.sign_raw_tx_with_wallet(raw_tx)

        assert re.match(r"^[0-9a-f]+$", signed_tx)

    def test_sign_raw_tx_with_wallet_ignore_raw_tx(self):
        params = self.__create_default_params()
        myTx = Transaction(params)

        with pytest.raises(RuntimeError):
            myTx.sign_raw_tx_with_wallet("ignore_raw_tx")

    def test_create_signed_tx(self):
        params = self.__create_default_params()
        myTransaction = Transaction(params)

        signed_tx = myTransaction.create_signed_tx()

        assert re.match(r"^[0-9a-f]+$", signed_tx)

        # ブロードキャストして確認 - 失敗時は例外がスローされてテスト失敗
        cmd = "bitcoin-cli -regtest sendrawtransaction " + signed_tx
        self.__run_command(cmd)
