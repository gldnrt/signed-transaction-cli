from st_cli.cli import demo


def test_demo(capfd):
    demo()

    out, err = capfd.readouterr()
    assert out == "Hello World!\n"
    assert err is ""
