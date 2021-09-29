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

    log=[]
    try:
        # テーブルへのPut処理実行
        quiz_table.put_item(
            Item = {
                "quiz_num": int(number), 
                "quiz_sentense": sentense,
                "answer": answer,
                "category": category,
                "img_file_name": img_file_name
            }
        )
        log.append('Edited! ['+str(data_index)+'],'+sentense+','+answer+',0,0,'+category+','+imgfilename)
    except ClientError as ce:
        log.append('Error. Pushing Index['+str(data_index)+'] Data Failed. :'+str(ce))
        break
    except TypeError as e:
        log.append(str(e))
    except Exception as e:
        log.append(str(e))

    return {
        'statusCode': 200,
        'log': log
    }
