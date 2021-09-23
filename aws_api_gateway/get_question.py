# -*- coding: utf-8 -*-
import boto3
import json
import configparser
import ini

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    try:
        # 設定ファイルからcsv名のリストを取得
        csv_name_list = ini.get_csv_name_list()
        # 設定ファイルからcsv名のリストを取得
        csv_file_name_list = ini.get_csv_file_name_list()
    
        #(ファイルID)-(問題番号)の形でリクエスト来るので取り出す
        req=event['text']
        file_id,quiz_id=map(int,req.split('-'))
    
        #テーブル選択
        #設定ファイルからファイルIDをもとにテーブル名を取り出す
        table    = dynamodb.Table(csv_file_name_list[file_id]) 
    
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
        quiz_sentense="["+csv_name_list[file_id]+"-"+str(response['Item']['quiz_num'])+"]:"+response['Item']['quiz_sentense']+accuracy
    
        #答えの文作成
        quiz_answer="["+csv_name_list[file_id]+"-"+str(response['Item']['quiz_num'])+"]答:"+response['Item']['answer']
    
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
            'error_log': 'Internal Server Error.'
        }
    
        return res
        
