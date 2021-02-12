# csv_quiz_bot

csvをクイズのデータベースとし、問題をslackに投稿する
slackからの応答はAWS API Gateway/Lambda/DynamoDBを利用し行う
完全に個人用

## select_quiz.py

指定したcsvファイル内の問題から入力した問題番号の問題を取得してslackに投稿するスクリプト
引数：問題番号


## random_quiz.py

指定したcsvファイル内の問題からランダムに１問取得してslackに投稿するスクリプト
引数なし

## worst_quiz.py

csvファイル内の問題から、正解率ワースト1~xの問題のうちランダムに１問取得してslackに投稿するスクリプト
xは設定ファイル(quiz.ini)のWORST_GROUP_NUMで指定
引数なし

## result_inputter.py

DB(API Gateway/Lambda/AWS DynamoDB)から問題の正解不正解データを取得し
csvに正解数データを更新するスクリプト
引数なし

## category_accuracy_list.py

csvにある問題を、カテゴリ毎に平均正解率を算出して表示するスクリプト

## random_category.py

category_accuracy_list.pyで作成したカテゴリリストを元に、
ランダムにカテゴリを選んで、そのカテゴリに属する問題を数問選んでslackに投稿するスクリプト

## search_quiz.py

語句を入力し、その語句が問題文または正解文に含まれている問題を表示するスクリプト
引数に検索語句を入力する

# csvのファイル形式

```
問題番号,問題文,答え,正解数,不正解数,カテゴリ
```

- カテゴリは、コロン(:)区切りで何個でも入力可能。