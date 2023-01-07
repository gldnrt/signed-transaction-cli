#!/bin/bash -ex

# regtest環境の初期化を行う
# 前提: Bitcoin Coreがインストール済みであること
# https://bitcoin.org/en/download

# delete old data
bitcoin-cli stop || true
sleep 1
pkill bitcoind || true
sleep 1
rm -rf ~/.bitcoin/regtest

# start bitcoind
bitcoind -daemon -conf=/home/dev/.bitcoin/bitcoin_regtest.conf
sleep 1

# create wallet
bitcoin-cli -regtest createwallet test_wallet




