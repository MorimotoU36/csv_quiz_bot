# -*- coding: utf-8 -*-
import boto3
import json
import configparser
import ini

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    # 設定ファイルからcsv名のリストを取得
    csv_name_list = ini.get_csv_name_list()

    #返り値作成(JSON)
    res = {
        'text': csv_name_list
    }

    return res
