import pytest
from st_cli.cli import get_params, check_params


def test_read_params():
    argv = [
        "./signed-transaction-cli/st_cli/__main__.py",
        "./tests/test_params/params.json",
    ]
    params = get_params(argv)

    assert params["utx"]["txid"] == "value-of-txid"
    assert params["utx"]["vout"] == "value-of-vout"
    assert params["utx"]["scriptPubKey_hex"] == "value-of-scriptPubKey_hex"


def test_no_args():
    argv = [
        "./signed-transaction-cli/st_cli/__main__.py",
    ]

    with pytest.raises(ReferenceError) as e:
        get_params(argv)

    assert str(e.value) == "Usage: st_cli [FILE_PATH]"


def test_too_many_args():
    argv = [
        "./signed-transaction-cli/st_cli/__main__.py",
        "./tests/test_params/params.json",
        "./tests/test_params/params.json",
    ]

    with pytest.raises(ReferenceError) as e:
        get_params(argv)

    assert str(e.value) == "Usage: st_cli [FILE_PATH]"


def test_no_existed_file():
    argv = [
        "./signed-transaction-cli/st_cli/__main__.py",
        "./no_existed.json",
    ]

    with pytest.raises(ReferenceError) as e:
        get_params(argv)

    assert str(e.value).startswith("Error: ignore params file,")


def test_incorrect_json():
    argv = [
        "./signed-transaction-cli/st_cli/__main__.py",
        "./tests/test_params/incorrect.json",
    ]

    with pytest.raises(ReferenceError) as e:
        get_params(argv)

    assert str(e.value).startswith("Error: ignore params file, ")


class TestCheckParams:
    '''check_paramsテストクラス'''

    def create_default_params(self) -> str:
        '''正常値のpaarm作成'''
        
        params = {
                "network": "regtest",
                "remittance_amount": 0.0,
                "transaction_fee": 0.00000,
                "specified_utxo": {
                    "txid": "09af",
                    "vout": 0,
                    "amount": 0
                },
                "address": {
                    "destination": "azAZ09",
                    "sender_charge": "90ZAza"
                }
            }
        return params

    def test_check_params(self):
        params = self.create_default_params()
        check_params(params)

    @pytest.mark.parametrize("network", ["regtest", "testnet", "mainnet"])
    def test_check_params_network(self, network):
        params = self.create_default_params()
        params["network"] = network

        check_params(params)

    # "params[key]: value"で指定できる値で、
    # 無効となるキーと値を
    # (key, value)形式のリストにする
    ignore_key_value = [
        ("network", 1),
        ("network", "ignore"),
        ("remittance_amount", -1),
        ("remittance_amount", "0"),
        ("transaction_fee", -1),
        ("transaction_fee", "0"),
    ]

    @pytest.mark.parametrize("key, value", ignore_key_value)
    def test_check_params_ignore_value(self, key, value):
        params = self.create_default_params()
        params[key] = value

        with pytest.raises(RuntimeError):
            check_params(params)

    # "params[parentkey][key]: value"で指定できる値で、
    # 無効となるキーと値を
    # (parentkey, key, value)形式のリストにする
    ignore_nestedkey_value = [
        ("specified_utxo", "txid", 0),
        ("specified_utxo", "txid", "g"),
        ("specified_utxo", "txid", "0g"),
        ("specified_utxo", "txid", "A"),
        ("specified_utxo", "vout", -1),
        ("specified_utxo", "vout", 0.1),
        ("specified_utxo", "vout", "0"),
        ("address", "destination", 0),
        ("address", "destination", ")"),
        ("address", "destination", "0)"),
        ("address", "sender_charge", 0),
        ("address", "sender_charge", ")"),
        ("address", "sender_charge", "0)"),
    ]

    @pytest.mark.parametrize("parentkey, key, value", ignore_nestedkey_value)
    def test_check_params_ignore_value_nested_key(self, parentkey, key, value):
        params = self.create_default_params()
        params[parentkey][key] = value

        with pytest.raises(RuntimeError) as e:
            check_params(params)

        print(e)
