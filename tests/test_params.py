import pytest
from st_cli.params import \
    check_params, read_params_from_file, get_params


class TestReadParamsFromFile:
    '''params.read_params_from_file()のテストクラス'''

    def test_read_params(self):
        param_file_path = "./tests/test_params/test_params.json"
        params = read_params_from_file(param_file_path)

        assert params["utx"]["txid"] == "value-of-txid"
        assert params["utx"]["vout"] == "value-of-vout"
        assert params["utx"]["scriptPubKey_hex"] == "value-of-scriptPubKey_hex"

    def test_no_existed_file(self):
        param_file_path = "./no_existed.json"

        with pytest.raises(ReferenceError) as e:
            get_params(param_file_path)

        assert str(e.value).startswith("Error: ignore params file,")

    def test_incorrect_json(self):
        param_file_path = "./tests/test_params/incorrect.json_"

        with pytest.raises(ReferenceError) as e:
            get_params(param_file_path)

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

    '''
    下記の内、異常値となる文字列を検出できることをテストする
    数値: 整数、浮動小数点、schcema定義範囲外の数値
    文字列: [0-9]+、[0-9a-z]+,[0-9a-zA-Z]+、記号を含む文字列、
            正常文字と以上文字の組み合わせ
    '''

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


class TestGetParams:
    '''get_paramsテストクラス'''

    def test_normal_case(self):
        params = get_params("./tests/test_params/correct_params.json")
        assert params["remittance_amount"] == 0.00008047

    def test_call_check_params(self):
        with pytest.raises(RuntimeError) as e:
            get_params("./tests/test_params/illigal_value_params.json")

        assert str(e.value).startswith("Error: ignore params file, ")




