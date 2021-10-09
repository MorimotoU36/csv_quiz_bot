# -*- coding: utf-8 -*-
import boto3
import json
import configparser
import random

client = boto3.client('dynamodb')

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    try:
        #テーブル名
        table_name='english_speaking'

        #全データの個数
        total_num = int(client.describe_table(TableName=table_name)['Table']['ItemCount'])

        #問題番号,ランダムフラグを取り出す
        quiz_id=int(event['text'])
        random_flag=bool(event['random'])

        if(not random_flag and (quiz_id < 1 or total_num < quiz_id)):
            #エラー、返り値作成(JSON)
            res = {
                'statusCode': 500,
                'sentense': '',
                'answer': '',
                'question_category': '',
                'error_log': 'Internal Server Error,問題番号は1~'+str(total_num)+'の間で入力してください'
            }
            return res
        elif(random_flag):
            #問題番号をランダムに取得
            quiz_id = random.randint(1,total_num)

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
        quiz_sentense="[和文英訳-"+str(response['Item']['quiz_num'])+"]:"+response['Item']['quiz_sentense']+accuracy

        #答えの文作成
        quiz_answer="[和文英訳-"+str(response['Item']['quiz_num'])+"]答:"+response['Item']['answer']

        #返り値作成(JSON)
        res = {
            'statusCode': 200,
            'sentense': quiz_sentense,
            'answer': quiz_answer,
            'quiz_id': quiz_id,
            'question_sentense': str(response['Item']['quiz_sentense']),
            'question_answer': str(response['Item']['answer']),
            'question_category': str(response['Item'].get('category','')),
            'question_img_file_name': str(response['Item'].get('img_file_name',""))
        }

        return res
    except:
        #返り値作成(JSON)
        res = {
            'statusCode': 500,
            'sentense': '',
            'answer': '',
            'question_category': '',
            'error_log': 'Internal Server Error'
        }
    
        return res