# -*- coding: utf-8 -*-
import pymysql
import pymysql.cursors
import traceback

from ini import get_ini_parser, get_messages_ini

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

# 指定したファイル番号からファイル名などの情報を取得
def get_file_info(conn,file_num):
    try:
        with conn.cursor() as cursor:
            sql = "SELECT file_num, file_name, file_nickname FROM quiz_file WHERE file_num = {0} ".format(file_num)
            cursor.execute(sql)
            sql_results = cursor.fetchall()

            if(len(sql_results) > 0):
                return {
                    "statusCode": 200,
                    "result": sql_results[0]
                }
            elif(len(sql_results) == 0):
                return {
                    "statusCode": 404,
                    "result": sql_results
                }
    except Exception as e:
        messages = get_messages_ini()
        return {
            "statusCode": 500,
            "message": messages['ERR_0004'],
            "traceback": traceback.format_exc()
        }

# 全ファイルの情報を取得
def get_all_file_info():
    # メッセージ設定ファイルを呼び出す
    messages = get_messages_ini()

    # MySQL への接続を確立する
    try:
        conn = get_connection()
    except Exception as e:
        return {
            "statusCode": 500,
            "message": messages['ERR_0002'],
            "traceback": traceback.format_exc()
        }

    try:
        with conn.cursor() as cursor:
            sql = "SELECT file_num, file_name, file_nickname FROM quiz_file ORDER BY file_num "
            cursor.execute(sql)
            sql_results = cursor.fetchall()

            if(len(sql_results) > 0):
                return {
                    "statusCode": 200,
                    "result": sql_results
                }
            elif(len(sql_results) == 0):
                return {
                    "statusCode": 404,
                    "result": sql_results
                }
    except Exception as e:
        messages = get_messages_ini()
        return {
            "statusCode": 500,
            "message": messages['ERR_0004'],
            "traceback": traceback.format_exc()
        }