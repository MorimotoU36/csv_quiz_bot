# csv_quiz_bot

csvをクイズのデータベースとし、問題をslackに投稿する
slackからの応答はAWS API Gateway/Lambda/DynamoDBを利用し行う
完全に個人用

## random_quiz.py

指定したcsvファイル内の問題からランダムに１問取得してslackに投稿するスクリプト
引数なし

## result_inputter.py

DB(API Gateway/Lambda/AWS DynamoDB)から問題の正解不正解データを取得し
csvに正解数データを更新するスクリプト
引数なし

## category_accuracy_list.py

csvにある問題を、カテゴリ毎に平均正解率を算出して表示するスクリプト


# csvのファイル形式

```
問題番号,問題文,答え,正解数,不正解数,カテゴリ
```

- カテゴリは、コロン(:)区切りで何個でも入力可能。