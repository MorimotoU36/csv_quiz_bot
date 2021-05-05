# csv_quiz_bot

csvをクイズのデータベースとし、問題をslackに投稿する
slackからの応答はAWS API Gateway/Lambda/DynamoDBを利用し行う
完全に個人用

## select_quiz.py

指定したcsvファイル内の問題から入力した問題番号の問題を取得してslackに投稿するスクリプト
引数：問題番号


## random_quiz.py

指定したcsvファイル内の問題からランダムに１問取得してslackに投稿するスクリプト
引数なし（オプション指定しない場合）

### オプション

- -n 数値,--number 数値 ・・・ 指定した数の分だけ問題を出題する

## worst_quiz.py

csvファイル内の問題から、正解率ワースト1~xの問題のうちランダムに１問取得してslackに投稿するスクリプト
xは設定ファイル(quiz.ini)のWORST_GROUP_NUMで指定
引数なし（オプション指定しない場合）

### オプション

- -n 数値,--number 数値 ・・・ ワースト1位~(指定した数)位の問題を順に出題する

## result_inputter.py

DB(API Gateway/Lambda/AWS DynamoDB)から問題の正解不正解データを取得し
csvに正解数データを更新するスクリプト
引数なし

また、以下バックアップファイルを作成する
- (csvファイル名).bkup　・・・　正解数データを更新する前のcsvファイル
- DB_bkup.csv　・・・　DBから取ってきた正解不正解データのcsvファイル

## category_accuracy_list.py

csvにある問題を、カテゴリ毎に平均正解率を算出して表示するスクリプト

### オプション

- -s,--sort ・・・ 平均正解率順にソートして表示

## random_category.py

category_accuracy_list.pyで作成したカテゴリリストを元に、
ランダムにカテゴリを選んで、そのカテゴリに属する問題を数問選んでslackに投稿するスクリプト

### オプション

- -w,--worst ・・・ ランダムではなく、一番正解率が悪いカテゴリを選ぶ

## search_quiz.py

語句を入力し、その語句が問題文または正解文に含まれている問題を表示するスクリプト
引数に検索語句を入力する

### オプション

- -i,--ignorecase ・・・ 半角英字の大文字小文字を無視して検索する

## minimum_correct_quiz.py

最も正解数の低い問題(複数ある場合はランダム)をslackに投稿するスクリプト
引数なし（オプション指定しない場合）

### オプション

- -n 数値,--number 数値 ・・・ 正解数ワースト1位~(指定した数)位の問題を順に出題する


## select_quiz_by_list.py

問題番号を列挙したリスト(別ファイル、config/select_quiz_num.dat)から問題番号を取り出し、その中からランダムに出題する
引数なし


## answer_inputter.py

問題に正解したかのデータを登録するためのスクリプト
[問題番号 正解(0)不正解(1)データ]のペアを複数引数に入力して実行する。ペアは何個でも入力可能


# csvのファイル形式

## 問題ファイル(csv)

```
問題番号,問題文,答え,正解数,不正解数,カテゴリ
```

- カテゴリは、コロン(:)区切りで何個でも入力可能。


## select_quiz_num.dat

```
問題番号
```

- 問題番号１列のみ。


# 設定ファイル

## quiz.ini

```
[Filename]
QUIZ_FILE_NAME=[(クイズ問題が書かれたファイル名,,,)]
QUIZ_INDEX_LIST=(ランダムに出題したい問題番号を羅列したファイル名)
DEFAULT_QUIZ_FILE_NUM=(出題したい問題ファイルのQUIZ_FILE_NAMEでのインデックス)

[Slack]
SLACK_API_URL=(SlackのチャンネルにメッセージをPOSTするためのURL)
SLACK_API_TOKEN=(SlackのチャンネルにメッセージをPOSTするためのアクセストークン)
SLACK_CHANNEL=(クイズを出題するためのSlackのチャンネル名)
SLACK_ANSWER_CHANNEL=(クイズの解答をPOSTするためのSlackのチャンネル名)
THINKING_TIME=(クイズ出題~解答をPOSTするための時間[秒])
WORST_GROUP_NUM=5

[AWS]
ANSWER_REGISTER_API=(回答を登録するためのAWSのAPI)
RESULT_GET_API=(回答を取得するためのAWSのAPI)
```