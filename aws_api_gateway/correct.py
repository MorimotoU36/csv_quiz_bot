# -*- coding: utf-8 -*-
import boto3
import json
import configparser
import ini

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    try:
        # 設定ファイルからcsv名のリストを取得
        csv_file_name_list = ini.get_csv_file_name_list()
        csv_name_list = ini.get_csv_name_list()
    
        #(ファイルID)-(問題番号)の形でリクエスト来るので取り出す
        req=event['text']
        file_id=req.split('-')[0] if req[0]=='E' else int(req.split('-')[0])
        quiz_id=int(req.split('-')[1])
        
        #テーブル名、csv名もここで取り出す
        table_name='english_speaking' if file_id=='E' else csv_file_name_list[file_id]
        csv_name="和文英訳" if file_id=='E' else csv_name_list[file_id]

        #テーブル選択
        #設定ファイルからファイルIDをもとにテーブル名を取り出す
        table    = dynamodb.Table(table_name) 
    
        #指定したテーブルに問題を取得しに行く
        response = table.get_item(
            Key={
                'quiz_num': quiz_id
            }
        )
    
        #正解数を取得して+1して更新
        correct = int(response['Item']['clear_count'])
        correct+=1
        req = table.update_item(
            Key={
                'quiz_num': quiz_id
            },
            UpdateExpression='SET clear_count = :val1',
            ExpressionAttributeValues={
                ':val1': correct
            }
        )
    
        #返り値作成(JSON)
        res = {
            'statusCode': 200,
            'message': "["+csv_name+"-"+str(quiz_id)+"] Cleared!!"
        }
    
        return res
    except:
        #返り値作成(JSON)
        res = {
            'statusCode': 500,
            'message': "",
            'error_log': 'Internal Server Error.'

        }
    
        return res