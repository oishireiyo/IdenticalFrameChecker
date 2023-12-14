# IdenticalFrameChecker
このrepositoryは、2つの動画(source video & target video)を入力に取り、target videoの各フレームがsource videoのどのフレームと完全に一致するかを返すWebアプリケーションです。フロントエンド側では、Reactを利用しUIを作成しています。一方バックエンド側ではFlaskを用い、エンドポイントを設定しています。

## はじめに
今の所特に書く事なし

## このRepositoryを更新したい
frontendとbackendの設定が必要です。

### frontend
Node.jsとnpmのインストールを行います。
```bash
apt-get update && apt-get upgrade
apt-get install nodejs npm
npm -g install n
n stable
apt-get purge nodejs npm
```
その後に、必要なパッケージをインストールし、完了後開発サーバーを立てます。
```bash
cd path/to/frontend
npm ci
npm run dev
```

### backend
pythonの設定を行い、完了後開発サーバーを立てます。
```
cd path/to/backend

```

## このRepositoryを使用したい
`docker-compose.yml`を利用し、`backend/Dockerfile`、`frontend/Dockerfile`と`nginx/Dockerfile`からイメージ、コンテナを作成します。
```bash
cd path/to/root/
docker-compose up --build
```
その後, [`http://127.0.0.1:8080`](http://127.0.0.1:8080)からアプリケーションを利用できます。

また、`backend`と`frontend`それぞれを個別に利用したい場合は、`Dockerfile`からイメージ、コンテナを作成してください。その際は、コンテナで使用しているポート番号を確認してください。

## 特記事項
- WSGIサーバーとして、`gunicorn`を使用しているが`optparse`との相性が悪いのか実行すると以下のエラーが発生する。
  ```bash
  $ gunicorn -b 127.0.0.1:8000 server:app
  [2023-12-13 02:03:27 +0900] [78862] [INFO] Starting gunicorn 21.1.0
  [2023-12-13 02:03:27 +0900] [78862] [INFO] Listening at: http://127.0.0.1:8000 (78862)
  [2023-12-13 02:03:27 +0900] [78862] [INFO] Using worker: sync
  [2023-12-13 02:03:27 +0900] [78863] [INFO] Booting worker with pid: 78863
  Usage: gunicorn [options]

  gunicorn: error: no such option: -b
  ```
  何故か原因は不明だが、コンテナ内で環境変数を設定してポート番号を渡すことで、`optparse`の利用を回避した。
