import pytest
from st_cli.cli import get_params_file_path, cli_main


class TestGetParamsFilePath:
    '''get_params_file_path()のテスト'''

    def test_normal_case(self):
        argv = [
            "./signed-transaction-cli/st_cli/__main__.py",
            "./tests/test_params/params.json",
        ]

        file_path = get_params_file_path(argv)
        assert file_path == "./tests/test_params/params.json"

    def test_no_args(self):
        argv = [
            "./signed-transaction-cli/st_cli/__main__.py",
        ]

        with pytest.raises(ReferenceError) as e:
            get_params_file_path(argv)

        assert str(e.value) == "Usage: st_cli [FILE_PATH]"

    def test_too_many_args(self):
        argv = [
            "./signed-transaction-cli/st_cli/__main__.py",
            "./tests/test_params/params.json",
            "./tests/test_params/params.json",
        ]

        with pytest.raises(ReferenceError) as e:
            get_params_file_path(argv)

        assert str(e.value) == "Usage: st_cli [FILE_PATH]"


class TestCliMain:
    '''cli_main()のテスト'''

    def test_exit_code(self, capfd):
        with pytest.raises(SystemExit) as e:
            cli_main(["./signed-transaction-cli/st_cli/__main__.py"])

        out, err = capfd.readouterr()
        assert out == ""
        assert err == "Usage: st_cli [FILE_PATH]\n"
        assert e.value.code == 1
