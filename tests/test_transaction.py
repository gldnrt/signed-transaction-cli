import json
import pytest
import re
from st_cli.transaction import Transaction
from . import testlib


class TestTransaction:
    '''
    Transactionテストクラス
    前提: walletがロードされていること
    '''

    def test_constructor_regtest(self):
        params = {"network": "regtest"}

        myTx = Transaction(params)

        assert myTx.params == params
        assert myTx.network_arg == "-regtest"

    def test_create_raw_tx(self):
        params = testlib.create_default_params()
        myTx = Transaction(params)

        raw_tx = myTx.create_raw_tx()

        assert re.match(r"^[0-9a-f]+$", raw_tx)

        # 結果をdecodeして確認する
        cmd = "bitcoin-cli -regtest decoderawtransaction " + raw_tx
        decoded_raw_tx = json.loads(testlib.run_command(cmd))
        print(decoded_raw_tx)

        assert len(decoded_raw_tx["vin"]) == 1
        assert decoded_raw_tx["vin"][0]["txid"]\
            == params["specified_utxo"]["txid"]
        assert decoded_raw_tx["vin"][0]["vout"]\
            == params["specified_utxo"]["vout"]

        assert len(decoded_raw_tx["vout"]) == 2
        assert decoded_raw_tx["vout"][0]["value"]\
            == params["remittance_amount"]
        assert decoded_raw_tx["vout"][0]["scriptPubKey"]["address"]\
            == params["address"]["destination"]
        assert decoded_raw_tx["vout"][1]["value"]\
            == pytest.approx(params["specified_utxo"]["amount"]
               - params["remittance_amount"]
               - params["transaction_fee"])
        assert decoded_raw_tx["vout"][1]["scriptPubKey"]["address"]\
            == params["address"]["sender_charge"]

    def test_create_raw_tx_ignore_param(self):
        params = testlib.create_default_params()
        params['specified_utxo']['txid'] = 'ignore_txid'
        myTx = Transaction(params)

        with pytest.raises(RuntimeError):
            myTx.create_raw_tx()

    def test_sign_raw_tx_with_wallet(self):
        params = testlib.create_default_params()
        myTx = Transaction(params)
        raw_tx = myTx.create_raw_tx()

        signed_tx = myTx.sign_raw_tx_with_wallet(raw_tx)

        assert re.match(r"^[0-9a-f]+$", signed_tx)

    def test_sign_raw_tx_with_wallet_ignore_raw_tx(self):
        params = testlib.create_default_params()
        myTx = Transaction(params)

        with pytest.raises(RuntimeError):
            myTx.sign_raw_tx_with_wallet("ignore_raw_tx")

    def test_create_signed_tx(self):
        params = testlib.create_default_params()
        myTransaction = Transaction(params)

        signed_tx = myTransaction.create_signed_tx()

        assert re.match(r"^[0-9a-f]+$", signed_tx)

        # ブロードキャストして確認 - 失敗時は例外がスローされてテスト失敗
        cmd = "bitcoin-cli -regtest sendrawtransaction " + signed_tx
        testlib.run_command(cmd)
