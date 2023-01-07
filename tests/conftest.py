import pytest
from . import testlib


@pytest.fixture(scope="session", autouse=True)
def create_coin():
    '''
    送金用コイン作成
    前提: walletがロードされていること
    '''

    cmd = (
        "bitcoin-cli -regtest generatetoaddress 101 "
        + '$(bitcoin-cli -regtest getnewaddress "sender")'
    )
    testlib.run_command(cmd)
