# -*- coding: utf-8 -*-
import boto3
import json
import configparser

client = boto3.client('dynamodb')

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    try:
        #テーブル名
        table_name='english_speaking'

        #全データの個数
        total_num = int(client.describe_table(TableName=table_name)['Table']['ItemCount'])

        #(問題番号)を取り出す
        quiz_id=int(event['text'])
        random_flag=bool(event['random'])

        #テーブル選択
        #設定ファイルからファイルIDをもとにテーブル名を取り出す
        table    = dynamodb.Table(table_name) 

        #指定したテーブルに問題を取得しに行く
        response = table.get_item(
            Key={
                'quiz_num': quiz_id
            }
        )

        correct_num=int(response['Item']['clear_count'])
        incorrect_num=int(response['Item']['fail_count'])
        correctrate= "{:.2f}".format(100*correct_num/(correct_num+incorrect_num)) if correct_num+incorrect_num!=0 else "0"
        rate=" (正解率:"+ correctrate + "%)" if correct_num+incorrect_num!=0 else " (未回答)" 

        #問題文作成
        accuracy="(正答率:{0:.2f}%)".format(100*correct_num/(correct_num+incorrect_num)) if (correct_num+incorrect_num)>0 else "(未回答)"
        quiz_sentense="[English-"+str(response['Item']['quiz_num'])+"]:"+response['Item']['quiz_sentense']+accuracy

        #答えの文作成
        quiz_answer="[English-"+str(response['Item']['quiz_num'])+"]答:"+response['Item']['answer']

        #返り値作成(JSON)
        res = {
            'statusCode': 200,
            'sentense': quiz_sentense,
            'answer': quiz_answer
        }

        return res
    except:
        #返り値作成(JSON)
        res = {
            'statusCode': 500,
            'sentense': '',
            'answer': '',
            'error_log': 'Internal Server Error'
        }
    
        return res