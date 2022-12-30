import pytest
from st_cli.cli import get_params


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


def test_too_many_args():
    argv = [
        "./signed-transaction-cli/st_cli/__main__.py",
        "./no_existed.json",
    ]

    with pytest.raises(ReferenceError) as e:
        get_params(argv)

    assert str(e.value) == "Error: ignore params file, ./no_existed.json"


def test_incorrect_json():
    argv = [
        "./signed-transaction-cli/st_cli/__main__.py",
        "./tests/test_params/incorrect.json",
    ]

    with pytest.raises(ReferenceError) as e:
        get_params(argv)

    assert (
        str(e.value) == "Error: ignore params file, ./tests/test_params/incorrect.json"
    )
