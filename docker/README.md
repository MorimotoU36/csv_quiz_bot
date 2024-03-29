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

2.1. テーブルを確認する

コンテナの初期作成時にinit.sqlでテーブルが作られることになっているが
作られていなかったらコンテナに入って作成する

```
$ docker exec -it (コンテナ名) /bin/bash
$ cd /docker-entrypoint-initdb.d
$ mysql -u root -p quiz_db < init.sql 
```

2.2. CSVデータをテーブルにインポートする

initdb.d ディレクトリにcsvを配置する

コンテナに入ってinitdb.dと同期しているディレクトリへいく

```
$ docker exec -it (コンテナ名) /bin/bash
$ cd /docker-entrypoint-initdb.d
```

まずMySQLにログイン

```
# mysql -u root -p
```

local_inifileの設定を見る

```
mysql> select @@local_infile;
+----------------+
| @@local_infile |
+----------------+
|              0 |
+----------------+
1 row in set (0.00 sec)
```

0ならば1にして出る

```
mysql> SET GLOBAL local_infile=on;
Query OK, 0 rows affected (0.00 sec)

mysql> select @@local_infile;
+----------------+
| @@local_infile |
+----------------+
|              1 |
+----------------+
1 row in set (0.00 sec)
```

コマンドラインから直接csv指定してインポートする
デリミタの指定も忘れずにする（デフォルトだとタブになるらしい）

```
$  mysqlimport -u root --password=pass --local --fields-terminated-by="," quiz_db aws_quiz.csv 
```

これを各csv毎でやる

3. Webページを確認

docker-composeでコンテナを起動したらローカルでサイトが起動されるので確認する

http://localhost:8080/pages/quiz.html

