# -*- coding: utf-8 -*-
import pymysql
import pymysql.cursors

from ini import get_ini_parser

def get_connection():
    """

    Returns:
        connections.Connectionn: MySQLへの接続子
    """

    # 設定ファイル読み込み
    config = get_ini_parser()

    connection = pymysql.connect(host=config['DATABASE']['hostname'],
                                user=config['DATABASE']['username'],
                                password=config['DATABASE']['password'],
                                db=config['DATABASE']['dbname'],
                                charset='utf8',
                                # 結果の受け取り方の指定。Dict形式で結果を受け取ることができる
                                cursorclass=pymysql.cursors.DictCursor)
    
    return connection

