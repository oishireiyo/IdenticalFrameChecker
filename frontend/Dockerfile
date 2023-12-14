FROM ubuntu:latest

# Docker build時に使用する変数
ARG EXPOSED_PORT=3210

# Docker container内で使用する環境変数の設定
ENV TZ=Asia/Tokyo \
  EXPOSED_PORT=${EXPOSED_PORT}

# work dirを用意
RUN mkdir -p /frontend/

# 現在のdirectoryにある全てのファイルをコピー
COPY . /frontend/

# 必要なモジュールのインストール
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    wget build-essential libbz2-dev libdb-dev libreadline-dev libffi-dev libgdbm-dev \
    liblzma-dev libncursesw5-dev libsqlite3-dev libssl-dev zlib1g-dev uuid-dev \
    nodejs npm \
  && npm -g install n \
  && n stable \
  && apt-get purge -y nodejs npm

# いらない物を消す
RUN apt-get autoremove -y

# work dirに移動し、必要なモジュールのインストール
# npm ciはローカルの環境と全く同じパッケージをインストールするので、npm installより再現性が高い。
WORKDIR /frontend/
RUN npm ci

# Docker container内で使用するポート番号
EXPOSE ${EXPOSED_PORT}

# コンテナ作成後に実行するコマンド
# 開発サーバーを使用する場合。
# 全てのネットワークからのアクセスを受け入れるため、HOSTを0.0.0.0に設定する。
# ポート番号はEXPOSEしたものと同一にする。
# CMD ./node_modules/.bin/webpack serve --open --host=0.0.0.0 --port=${EXPOSED_PORT}
# Nginxを利用する場合。
CMD ./node_modules/.bin/webpack .