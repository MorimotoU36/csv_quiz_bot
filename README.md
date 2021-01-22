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

# csvのファイル形式

```
問題番号,問題文,答え,正解数,不正解数
```