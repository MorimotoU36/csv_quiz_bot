# -*- coding: utf-8 -*-
import os
import sys
import random
import traceback
import pymysql
import pymysql.cursors

sys.path.append(os.path.join(os.path.dirname(__file__), '../module'))
from dbconfig import get_connection, get_file_info
from ini import get_messages_ini

def minimum_quiz(file_num=-1,category=None,checked=False):
    """最小正解数の問題を取得する

    Args:
        file_num (int, optional): ファイル番号. Defaults to -1.
        category (str, optional): カテゴリ. Defaults to None.
        checked (bool, optional): チェックした問題だけから出題するかのフラグ. Defaults to False.

    Returns:
        results [JSON]: 取得した問題
    """

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

    # ファイル番号からテーブル名を取得
    table_info = get_file_info(conn,file_num)
    if(table_info['statusCode'] == 200):
        nickname = table_info['result']['file_nickname']
    else:
        return {
            "statusCode": 400,
            "message": messages['ERR_0001']
        }
    
    # テーブル名からSQLを作成して投げる
    try:
        with conn.cursor() as cursor:
            # 指定したテーブルの正解数が最も低い問題を調べる
            # カテゴリが指定されている場合は条件文を追加する
            where_statement = [" file_num = {0} ".format(file_num)]

            # 削除済問題を取らない条件追加
            where_statement.append(" deleted != 1 ")

            if(category is not None):
                where_statement.append(" category LIKE '%"+category+"%' ")
            if(checked):
                where_statement.append(" checked != 0 ")
            
            if(len(where_statement) > 0):
                where_statement = ' WHERE ' + ' AND '.join(where_statement)
            else:
                where_statement = ''

            sql = "SELECT file_num, quiz_num, quiz_sentense, answer, clear_count, fail_count, category, img_file, checked, deleted, accuracy_rate FROM quiz_view " + where_statement +" ORDER BY clear_count LIMIT 1"
            cursor.execute(sql)

            # MySQLから帰ってきた結果を受け取る
            # Select結果を取り出す
            results = cursor.fetchall()
            # accuracy_rateはstr型にする(API)
            for ri in results:
                ri["accuracy_rate"] = str(0 if ri["accuracy_rate"] is None else round(ri["accuracy_rate"],1))

        # 結果をJSONに変形して返す
        return {
            "statusCode": 200,
            "result": results
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "message": messages['ERR_0004'],
            "traceback": traceback.format_exc()
        }

if __name__=="__main__":
    print("minimum_quiz!")