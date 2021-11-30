import json
import boto3
import urllib
import datetime

dynamodb = boto3.resource('dynamodb')
table    = dynamodb.Table('テーブル名')

def lambda_handler(event, context):
    # TODO implement
    payload=urllib.parse.unquote(event['body'])
    payload=json.loads(payload[8:])
    
    #slackボタンのvalueに"問題集番号-問題番号-正解不正解"とデータを定義
    file_id,quiz_id,flag=payload['actions'][0]['value'].split('-')
    print(file_id,quiz_id,flag)
    
    ## DynamoDBに解答データを登録
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
    
    return {
        'statusCode': 200,
        'body': json.dumps("["+str(file_id)+"-"+str(quiz_id)+"]"+payload['actions'][0]['name'])
    }


