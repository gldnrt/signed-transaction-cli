import re
import pytest
from st_cli import cli
from . import testlib


class TestGetParamsFilePath:
    '''get_params_file_path()のテスト'''

    def test_normal_case(self):
        argv = [
            "./signed-transaction-cli/st_cli/__main__.py",
            "./tests/test_params/params.json",
        ]

        file_path = cli.get_params_file_path(argv)
        assert file_path == "./tests/test_params/params.json"

    def test_no_args(self):
        argv = [
            "./signed-transaction-cli/st_cli/__main__.py",
        ]

        with pytest.raises(ReferenceError) as e:
            cli.get_params_file_path(argv)

        assert str(e.value) == "Usage: st_cli [FILE_PATH]"

    def test_too_many_args(self):
        argv = [
            "./signed-transaction-cli/st_cli/__main__.py",
            "./tests/test_params/params.json",
            "./tests/test_params/params.json",
        ]

        with pytest.raises(ReferenceError) as e:
            cli.get_params_file_path(argv)

        assert str(e.value) == "Usage: st_cli [FILE_PATH]"


class TestCliMain:
    '''
    cli_main()のテスト

    結合テストケース
    ・正常系: test_normal_case()
    ・引数エラー: test_error_occurred()
    ・設定ファイルがjson形式でない: test_input_file_not_json()
    ・設定ファイルが存在しない: test_input_file_not_exist()
    ・入力ファイルのValidation: test_check_input_file_schema()
        個々の項目はTestCheckParamsで行っているため省略
    ・異常値を含む入力ファイル
        - 無効なtxid: TestCliMain.test_ignore_txid()
    '''

    def test_normal_case(self, capfd):
        params = testlib.create_default_params()
        testlib.create_input_file(params)

        path = testlib.get_default_input_file_path()
        args = ["./st_cli/__main__.py", path]

        cli.cli_main(args)

        out, err = capfd.readouterr()
        assert re.match(r"^[0-9a-f]+$", out)
        assert err == ""

        # 片づけ
        testlib.delete_input_file()

    def test_error_occurred(self, capfd):
        with pytest.raises(SystemExit) as e:
            cli.cli_main(["./st_cli/__main__.py"])

        out, err = capfd.readouterr()
        assert out == ""
        assert err == "Usage: st_cli [FILE_PATH]\n"
        assert e.value.code == 1

    def test_input_file_not_json(self, capfd):
        with pytest.raises(SystemExit) as e:
            cli.cli_main([
                "./st_cli/__main__.py",
                "./tests/test_params/incorrect.json_"
            ])
            
        out, err = capfd.readouterr()
        assert out == ""
        assert err.startswith("Error: ignore params file,")
        assert e.value.code == 1

    def test_input_file_not_exist(self, capfd):
        with pytest.raises(SystemExit) as e:
            cli.cli_main([
                "./st_cli/__main__.py",
                "./tests/test_params/not/exist/param.json"
            ])
            
        out, err = capfd.readouterr()
        assert out == ""
        assert err.startswith("Error: ignore params file,")
        assert e.value.code == 1

    def test_check_input_file_schema(self, capfd):
        params = testlib.create_default_params()
        params['remittance_amount'] = -0.1

        testlib.create_input_file(params)

        path = testlib.get_default_input_file_path()
        args = ["./st_cli/__main__.py", path]

        with pytest.raises(SystemExit) as e:
            cli.cli_main(args)

        out, err = capfd.readouterr()
        assert out == ""
        assert err.startswith("Error: ignore params file,")
        assert e.value.code == 1

    def test_ignore_txid(self, capfd):
        params = testlib.create_default_params()
        params['specified_utxo']['txid'] = "0" * 64

        testlib.create_input_file(params)

        path = testlib.get_default_input_file_path()
        args = ["./st_cli/__main__.py", path]

        with pytest.raises(SystemExit) as e:
            cli.cli_main(args)

        out, err = capfd.readouterr()
        assert out == ""
        assert err.startswith("Error, sign raw transaction is not complete")
        assert e.value.code == 1


class TestCreateSignedTransaction:
    '''
    create_signed_transaction()のテスト
    '''

    args = []
    params = {}

    def setup_method(self):
        '''テストメソッドの準備'''

        path = testlib.get_default_input_file_path()
        self.args = ["./st_cli/__main__.py", path]
        self.params = testlib.create_default_params()

    def teardown_method(self):
        '''テストメソッドの後片付け'''
        try:
            testlib.delete_input_file()
        except Exception:
            pass

    def test_normal_case(self, capfd):
        testlib.create_input_file(self.params)
        
        cli.create_signed_transaction(self.args)
        
        out, err = capfd.readouterr()
        assert re.match(r"^[0-9a-f]+$", out)
        assert err == ""

    '''
    子モジュールでエラーとなる入力を行い、
    それぞれの子モジュールが呼ばれていることを確認する
    '''
    def test_calling_get_params_file_path_with_error(self, capfd):
        with pytest.raises(ReferenceError):
            cli.create_signed_transaction(["./st_cli/__main__.py"])

    def test_calling_get_params_with_error(self, capfd):
        self.params['network'] = "ignore"
        testlib.create_input_file(self.params)

        with pytest.raises(RuntimeError) as e:
            cli.create_signed_transaction(self.args)

        assert str(e.value).startswith("Error: ignore params file, ")

    def test_calling_create_signed_tx_with_error(self, capfd):
        self.params['specified_utxo']['txid'] = "000000000"
        testlib.create_input_file(self.params)

        with pytest.raises(RuntimeError) as e:
            cli.create_signed_transaction(self.args)

        assert str(e.value).startswith("Error, failed create raw transaction,")
