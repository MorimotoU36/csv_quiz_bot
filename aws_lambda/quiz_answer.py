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
        file_id,quiz_id,flag=0,0,0
        if('+' in text):
            text=re.sub(r'\++','+',text)
            text=list(text.split('+'))
            file_id,quiz_id,flag=text[0],text[1],text[2]
        else:
            #'+'無い場合はスペース区切り
            file_id,quiz_id,flag=text.split()
            
        
        #現在時刻取得
        dt_now = str(datetime.datetime.now())
        
        # quiz_answerへのPut処理実行
        table.put_item(
            Item = {
                "time": dt_now, 
                "file_id": file_id,
                "quiz_id": quiz_id, 
                "result": flag
            }
        )
        
        res="File["+str(file_id)+"] Question["+str(quiz_id)+"]:"+ ("Correct!" if flag != "0" else "Incorrect")
        return res
            
    except Exception as e:
        return str(text)+str(e)
