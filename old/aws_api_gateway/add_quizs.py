# -*- coding: utf-8 -*-
import boto3
import json
import configparser
import ini
from botocore.exceptions import ClientError

client = boto3.client('dynamodb')

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    #ファイル番号
    file_num=event['file']
    if(file_num!="E"):
        file_num=int(event['file'])
    
    #入力データ
    input_data=event['data'].splitlines()
    
    # 設定ファイルからcsv名のリストを取得
    csv_name_list = ini.get_csv_name_list()
    file_name_list = ini.get_csv_file_name_list()

    # 選択したcsvファイル名を取得
    file_name = "english_speaking" if file_num=="E" else file_name_list[file_num]
    # 現在選択したcsvファイルにあるデータの個数を取得
    data_index=int(client.describe_table(TableName=file_name)['Table']['ItemCount'])
    # 入力データを最初のインデックスにセット
    data_index+=1
    
    #DynamoDBテーブルを選択
    quiz_table = dynamodb.Table(file_name)
    
    log=[]
    for i,di in enumerate(input_data):
        #１行を各要素に分割
        di=list(di.split(','))
        #入力した１行が４項目未満なら入れないで飛ばす
        if(len(di)<4):
            log.append('Input Error. ['+str(i)+'L]: '+str(di))
            continue
        
        try:
            sentense=di[0]
            answer=di[1]
            category=di[2]
            imgfilename=di[3]

            # テーブルへのPut処理実行
            quiz_table.put_item(
                Item = {
                    "quiz_num": data_index, 
                    "quiz_sentense": sentense,
                    "answer": answer,
                    "clear_count": 0, 
                    "fail_count": 0, 
                    "category": category,
                    "img_file_name": imgfilename
                },
                ConditionExpression='attribute_not_exists(quiz_num)'
            )
            log.append('Added! ['+str(data_index)+'],'+sentense+','+answer+',0,0,'+category+','+imgfilename)
        except ClientError as ce:
            log.append('Error. Pushing Index['+str(data_index)+'] Data Failed. :'+str(ce))
            break
        except TypeError as e:
            log.append(str(e))
        except Exception as e:
            log.append(str(e))
        
        #問題番号を+1する
        data_index+=1
        
    
    return {
        'statusCode': 200,
        'log': log
    }
