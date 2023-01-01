# signed-transaction-cli

## 概要

Bitcoinの署名済み送金用トランザクションを作成するCLIアプリケーション  
オフライン環境で実行可能

## 実行環境

以下のOS/ライブラリを使用する

|  OS/ライブラリ  |  動作確認バージョン  |
| ---- | ---- |
|  Linux  |  Ubuntu22.04.1LTS  |
|  bitcoin core  |  v24.0.1  |
|  Python  |  3.10.6  |
|  Poetry  |  1.3.1  |


## インストール

`signed-transaction-cli`ディレクトリで、以下を実行する
```
$ poetry intall
```

## パラメータファイル

書式は以下

```
{
    "network": "接続先をregtest|testnet|mainnetから選択",
    "remittance_amount": 送金量,
    "transaction_fee": トランザクションfeeの量を指定,
    "unspent_transaction": {
        "txid": "送金に使用する未使用のトランザクションid",
        "vout": 送金に使用するvoutを指定,
        "value": 指定したvoutのvalue
    },
    "address": {
        "destination": "送金先アドレス",
        "sender_charge": "送金者への残額返金用アドレス"
    }
}

```

#### パラメータファイルのサンプル

[sample/params.json](./sample/params.json)を参照

## 実行

walletがロードされている状態で、以下を実行する

```
$ python3 -m st_cli [PARAM_FILE_PATH]
```
### 実行例

```
$ python3 -m st_cli ./params.json
aabbcc

```
#### ブロードキャスト結果の例

TODO: Link

## テスト

`signed-transaction-cli`ディレクトリで、以下を実行する

```
$ pytest
```