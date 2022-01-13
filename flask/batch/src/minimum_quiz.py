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

def minimum_quiz(file_num=-1,category=None,image=True):
    """最小正解数の問題を取得する

    Args:
        file_num (int, optional): ファイル番号. Defaults to -1.
        category (str, optional): カテゴリ. Defaults to None.
        image (bool, optional): イメージフラグ. Defaults to True.

    Returns:
        results [JSON]: 取得した問題
    """

    # 設定ファイルを呼び出してファイル番号からテーブル名を取得
    # (変なファイル番号の時はランダムに選ぶ)
    table_list = get_table_list()
    if(file_num < 0 or len(table_list) <= file_num):
        file_num = random.randint(0,len(table_list)-1)
    table = table_list[file_num]['name']
    nickname = table_list[file_num]['nickname']

    # TODO イメージフラグの操作
        
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
        # 指定したテーブルの正解数が最も低い問題を調べる
        # カテゴリが指定されている場合は条件文を追加する
        where_statement = "WHERE"
        if(category is not None):
            where_statement += " category LIKE '%"+category+"%' "
        
        if(where_statement == "WHERE"):
            where_statement = ""

        sql = "SELECT quiz_num, quiz_sentense, answer, clear_count, fail_count, category, img_file FROM {0} ".format(table) + where_statement +" ORDER BY clear_count LIMIT 1"
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
    res = minimum_quiz(file_num=0)
    print(res)