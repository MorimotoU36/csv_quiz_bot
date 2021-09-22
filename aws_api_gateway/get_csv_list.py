# -*- coding: utf-8 -*-
import boto3
import json
import configparser
import ini

client = boto3.client('dynamodb')

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    # 設定ファイルからcsv名のリストを取得
    csv_name_list = ini.get_csv_name_list()

    # 各csvにあるデータの個数のリストを取得
    file_name_list = ini.get_csv_file_name_list()
    item_list = []
    for ci in file_name_list:
        item_list.append(int(client.describe_table(TableName=ci)['Table']['ItemCount']))
    
    #返り値作成(JSON)
    res = {
        'text': csv_name_list,
        'item': item_list
    }
    
    return res
