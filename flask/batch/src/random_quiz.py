# -*- coding: utf-8 -*-
import os
import sys
import random
import traceback
import pymysql
import pymysql.cursors

sys.path.append(os.path.join(os.path.dirname(__file__), '../module'))
from dbconfig import get_connection
from ini import get_table_list

def random_quiz(file_num=-1,image=True,rate=100.0):
    """問題を１問、ランダムに取得するAPI

    Args:
        file_num (int, optional): ファイル番号. Defaults to -1.
        image (bool, optional): 画像取得フラグ. Defaults to True.
        rate (float, optional): 取得する問題の正解率の最大値. Defaults to 100.0.

    Returns:
        result (JSON): ランダムに取得した問題
    """
    # TODO image_flagの処理
    # TODO rateの処理

    # 設定ファイルを呼び出してファイル番号からテーブル名を取得
    # (変なファイル番号の時はランダムに選ぶ)
    table_list = get_table_list()
    if(file_num < 0 or len(table_list) <= file_num):
        file_num = random.randint(0,len(table_list)-1)
    table = table_list[file_num]['name']
    nickname = table_list[file_num]['nickname']
        
    # MySQL への接続を確立する
    try:
        conn = get_connection()
    except Exception as e:
        return {
            "statusCode": 500,
            "message": 'Error: DB接続時にエラーが発生しました',
            "traceback": traceback.format_exc()
        }
    
    # テーブル名からSQLを作成して投げる
    with conn.cursor() as cursor:
        # SQL作成して問題を取得する。結果のうちランダムに1つ取得する
        sql = "SELECT quiz_num, quiz_sentense, answer, clear_count, fail_count, category, img_file FROM {0} ORDER BY RAND() LIMIT 1".format(table)
        cursor.execute(sql)

        # MySQLから帰ってきた結果を受け取る
        # Select結果を取り出す
        results = cursor.fetchall()

    # 結果をJSONに変形して返す
    return {
        "statusCode": 200,
        "result": results
    }

if __name__=="__main__":
    res = random_quiz(file_num=-1)
    print(res)