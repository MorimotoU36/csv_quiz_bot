#
# AWS Lambda
# Slackから問題の正解不正解をDynamoDBに登録するコード
#
import boto3
import datetime
import re

dynamodb = boto3.resource('dynamodb')
table    = dynamodb.Table('テーブル名')

def lambda_handler(event, context):
    try:
        #slackから /register 問題ID 正解不正解フラグ(0なら不正解,それ以外なら正解)と来る
        #slackの入力(問題ID、正解不正解フラグ)からデータを取り出す
        #slackからだとスペースが'+'になる？
        text=event['text']
        quiz_id,flag=0,0
        if('+' in text):
            text=re.sub(r'\++','+',text)
            text=list(text.split('+'))
            quiz_id,flag=text[0],text[1]
        else:
            #'+'無い場合はスペース区切り
            quiz_id,flag=text.split()
            
        
        #現在時刻取得
        dt_now = str(datetime.datetime.now())
        
        # quiz_answerへのPut処理実行
        table.put_item(
            Item = {
                "time": dt_now, 
                "quiz_id": quiz_id, 
                "result": flag
            }
        )
        
        res="問題["+str(quiz_id)+"]:"+("正解" if flag != 0 else "不正解")
        return res
            
    except Exception as e:
        return str(text)+str(e)
