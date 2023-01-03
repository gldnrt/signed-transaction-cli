# signed-transaction-cli

## 概要

Bitcoinの署名済み送金用トランザクションを作成するアプリケーション  
* CLI
* オフライン環境で実行可能

## 実行環境

以下のOS/ライブラリを使用する

|  OS/ライブラリ  |  動作確認バージョン  |
| ---- | ---- |
|  Linux  |  WSL2 + Ubuntu22.04.1LTS  |
|  Bitcoin Core  |  v24.0.1  |
|  Python  |  3.10.6  |
|  Poetry  |  1.3.1  |


## インストール

```
$ cd signed-transaction-cli
$ poetry intall
```

## パラメータファイル

サンプルは[sample/params.json](./sample/params.json)を参照

書式は以下

```
{
    "network": "接続先をregtest|testnet|mainnetから選択",
    "remittance_amount": 送金量,
    "transaction_fee": トランザクションfeeの量を指定,
    "specified_utxo": {
        "txid": "送金に使用するUTXOのtxidを指定",
        "vout": 送金に使用するUTXOのvoutを指定,
        "amount": 送金に使用するUTXOのamountを指定
    },
    "address": {
        "destination": "送金先アドレス",
        "sender_charge": "送金者への残額返金用アドレス"
    }
}

```

## 実行

bitcoindの起動およびwalletがロードされている状態で、以下を実行する

```
$ python3 -m st_cli [PARAM_FILE_PATH]
```
### 実行例

1. `[PARAM_FILE_PATH]`に[sample/params.json](./sample/params.json)を指定する

```
$ python3 -m st_cli ./sample/params.json
020000000001019cfcb1d1d651010915656634cdd95350fb00d6506065c97a526aac0775cd80f40000000000fdffffff02d2040000000000001600144a0f48a8eb296723a16e30e685f4cbdda3ea3e84b51600000000000016001402f628d65bd80ab9b6c4079ab2eb5ed2f3cfa0d902473044022024ba00452a1b39d6afeae0061e8d85317354e2db475877cabdf164797ea58562022003a8f4fdd59c858f2ef7d2bea0ee6433107b9e2d342272a85dce62d41ef6adbc012103e04c91f9c0448a1c16bd134dd54a5425d1101481419ef7578472745e189401a600000000
```

署名済み送金用トランザクションが標準出力に出力された

#### testnetで確認

1. 上記トランザクションを以下のコマンドでブロードキャストする

```
$ bitcoin-cli -testnet sendrawtransaction 020000000001019...1a600000000
e666248e6f84d8c4c39652695d09a52d5f988ed1862de5d0db6845068ca4ee17e666248e6f84d8c4c39652695d09a52d5f988ed1862de5d0db6845068ca4ee17
```

3. 結果を確認する

[blockcypher.comの結果](https://live.blockcypher.com/btc-testnet/tx/e666248e6f84d8c4c39652695d09a52d5f988ed1862de5d0db6845068ca4ee17/)

上記URLで、[sample/params.json](./sample/params.json)の`"remittance_amount"`の値が
アドレス`destination`に送信されている

## テスト

`signed-transaction-cli`ディレクトリで、以下を実行する

```
$ poetry run pytest
```