# -*- coding: utf-8 -*-
import os
import sys
import traceback
import pymysql
import pymysql.cursors

sys.path.append(os.path.join(os.path.dirname(__file__), '../module'))
from dbconfig import get_connection, get_file_info
from ini import get_messages_ini

def select_quiz(file_num,quiz_num):
    """ファイル番号、問題番号から問題を取得する関数

    Args:
        file_num (int): ファイル番号
        quiz_num (int): 問題番号

        Returns:
            result (JSON): 取得した問題
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

    # テーブル名と問題番号からSQLを作成して投げる
    # (問題番号が範囲外なら終了)
    # SQLを実行する
    with conn.cursor() as cursor:
        # 指定したテーブルの件数を調べる
        sql = "SELECT count(*) FROM quiz WHERE file_num = {0}".format(file_num)
        cursor.execute(sql)
        results = cursor.fetchall()
        for r in results:
            count = r['count(*)']

        # 問題番号が範囲外なら終了
        if(quiz_num < 1 or count < quiz_num):
            return {
                "statusCode": 500,
                "message": messages['ERR_0003'].format(nickname,count)
            }

        sql = "SELECT file_num, quiz_num, quiz_sentense, answer, clear_count, fail_count, category, img_file, checked, deleted, accuracy_rate FROM quiz_view WHERE file_num = {0} AND quiz_num = {1}".format(file_num,quiz_num)
        cursor.execute(sql)

        # MySQLから帰ってきた結果を受け取る
        # Select結果を取り出す
        results = cursor.fetchall()

        # accuracy_rateはDecimal->str型にする(API)
        for ri in results:
            ri["accuracy_rate"] = str(0 if ri["accuracy_rate"] is None else round(ri["accuracy_rate"],1))

    # 結果をJSONに変形して返す
    return {
        "statusCode": 200,
        "result": results
    }

if __name__=="__main__":
    print("select_quiz!")