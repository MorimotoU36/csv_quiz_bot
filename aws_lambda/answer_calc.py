#
# AWS Lambda
# 正解不正解データを取ってきてcsvに正解/不正解数を登録する
#
import boto3

dynamodb = boto3.resource('dynamodb')
table    = dynamodb.Table('テーブル名')

def lambda_handler(event, context):
    try:
        #DynamoDB(quiz_result_list)へのscan処理実行
        response = table.scan()
        
        #0件なら処理終了
        if(len(response)==0):
            return []
        
        #scan結果からデータを取り出す
        records=list(response['Items'])
        
        # DynamoDBからレコード削除
        for r in records:
            table.delete_item(Key={'time': r['time']})
        
        return records
    except Exception as e:
        return e
