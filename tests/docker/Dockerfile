FROM python:3.10

# poetry
RUN pip install --upgrade pip && pip install poetry

# signed-transaction-cli
RUN git clone https://github.com/gldnrt/signed-transaction-cli.git
WORKDIR /signed-transaction-cli
RUN poetry install

# Bitcoin Core
ARG BITCOIN_CORE_VERSION=24.0.1
RUN curl -LO https://bitcoincore.org/bin/bitcoin-core-24.0.1/bitcoin-${BITCOIN_CORE_VERSION}-x86_64-linux-gnu.tar.gz
RUN tar -zxvf bitcoin-${BITCOIN_CORE_VERSION}-x86_64-linux-gnu.tar.gz
ENV PATH $PATH:/signed-transaction-cli/bitcoin-${BITCOIN_CORE_VERSION}/bin/

ADD ./bitcoin.conf /root/.bitcoin/
ENTRYPOINT ["bitcoind","-conf=/root/.bitcoin/bitcoin.conf"]
