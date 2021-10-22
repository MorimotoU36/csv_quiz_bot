# README

docker類の起動方法について

1. docker-composeによりコンテナ起動

当フォルダ内で下記コマンド実行

```
$ docker-compose up -d
```

するとイメージを取り寄せてコンテナを構築してくれる

2. VS CodeのMySQL拡張機能からコンテナ上のMySQLに接続する

接続情報は以下の通り。

```
ホスト名：127.0.0.1
ユーザ名：root
パスワード：pass
ポート番号：3306
データベース名：testdb
```