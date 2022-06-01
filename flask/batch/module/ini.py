# -*- coding: utf-8 -*-
import os
import json
import configparser

def get_ini_parser():
    """
    設定ファイルを読み込んで返す。設定ファイルのパスは環境変数INIから読み込む
    Returns:
        configparser.Configparser(): 読み込んだ設定ファイルの内容
    """
    # 設定ファイル読み込み
    config = configparser.ConfigParser()
    config.read(os.environ['INI'])

    return config

def get_table_list():
    """テーブル名のリストを示したJSONを返す

    Returns:
        json : テーブル名のリストを示したJSON
    """
    # テーブルのリストが書かれたJSONファイルを開く
    json_open = open(os.path.dirname(__file__)+'/table_list.json', 'r')
    # 開いたJSONファイルを読み込む
    json_load = json.load(json_open)
    json_open.close()
    # テーブルのリストJSONを返す
    return json_load['table']