# csv_quiz_bot

csvをクイズのデータベースとし、問題をslackに投稿する
slackからの応答はAWS API Gateway/Lambda/DynamoDBを利用し行う
完全に個人用


# csvのファイル形式

```
問題番号,問題文,答え,正解数,不正解数
```