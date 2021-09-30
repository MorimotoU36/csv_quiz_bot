# -*- coding: utf-8 -*-
import boto3
import json
import configparser
import ini
from botocore.exceptions import ClientError

client = boto3.client('dynamodb')

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    # 値取得
    file=event['file']
    number=event['number']
    file_num=event['file_num']
    sentense=event['sentense']
    answer=event['answer']
    category=event['category']
    img_file_name=event['img_file_name']

    # 設定ファイルからcsv名のリストを取得
    csv_name_list = ini.get_csv_name_list()
    file_name_list = ini.get_csv_file_name_list()

    # 選択したcsvファイル名を取得
    file_name = file_name_list[int(file_num)]

    #DynamoDBテーブルを選択
    quiz_table = dynamodb.Table(file_name)

    status_code=""
    message=""
    try:
        # テーブルへのUpdate処理実行
        quiz_table.update_item(
                Key={'quiz_num': int(number)},
                UpdateExpression="set #sentense = :quiz_sentense, #answer = :answer, #category = :category, #img_file_name = :img_file_name",
                ExpressionAttributeNames={
                    '#sentense': 'quiz_sentense',
                    '#answer': 'answer',
                    '#category': 'category',
                    '#img_file_name': 'img_file_name'
                },
                ExpressionAttributeValues={
                    ':quiz_sentense': sentense,
                    ':answer': answer,
                    ':category': category,
                    ':img_file_name': img_file_name
                },
                ReturnValues="UPDATED_NEW"
            )
        status_code = "200"
        message = 'Edited! ['+file+'-'+number+'],'+sentense+','+answer+',0,0,'+category+','+img_file_name
    except ClientError as ce:
        status_code = "500"
        message = 'Error. Pushing Index['+file+'-'+number+'] Data Failed. :'+str(ce)
    except TypeError as e:
        status_code = "500"
        message = 'Error. Pushing Index['+file+'-'+number+'] Data Failed. :'+str(e)
    except Exception as e:
        status_code = "500"
        message = 'Error. Pushing Index['+file+'-'+number+'] Data Failed. :'+str(e)

    return {
        'statusCode': status_code,
        'message': message
    }
