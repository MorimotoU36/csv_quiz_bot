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

def worst_quiz(file_num=-1,category=None,image=True):
    """最低正解率の問題を取得

    Args:
        file_num (int, optional): ファイル番号. Defaults to -1.
        category (str, optional): カテゴリ. Defaults to None.
        image (bool, optional): イメージフラグ. Defaults to True.

    Returns:
        results: 取得した問題
    """

    # 設定ファイルを呼び出してファイル番号からテーブル名を取得
    # (変なファイル番号の時はランダムに選ぶ)
    table_list = get_table_list()
    if(file_num < 0 or len(table_list) <= file_num):
        file_num = random.randint(0,len(table_list)-1)
    table = table_list[file_num]['name']
    view = table_list[file_num]['name']+'_view'
    nickname = table_list[file_num]['nickname']

    # TODO カテゴリを使った操作
    # TODO イメージフラグの操作
        
    # MySQL への接続を確立する
    try:
        conn = get_connection()
    except Exception as e:
        print('Error: DB接続時にエラーが発生しました')
        print(traceback.format_exc())
        sys.exit()
    
    # テーブル名からSQLを作成して投げる
    with conn.cursor() as cursor:
        # 指定したテーブルの正解率が最も低い問題を調べる
        sql = "SELECT quiz_num FROM {0} ORDER BY accuracy_rate LIMIT 1".format(view)
        cursor.execute(sql)
        results = cursor.fetchall()
        quiz_id = results[0]['quiz_num']

        # SQL作成して問題を取得する
        sql = "SELECT quiz_num, quiz_sentense, answer, clear_count, fail_count, category, img_file FROM {0} WHERE quiz_num = {1}".format(table,quiz_id)
        print(sql)
        cursor.execute(sql)

        # MySQLから帰ってきた結果を受け取る
        # Select結果を取り出す
        results = cursor.fetchall()

    # 結果をJSONに変形して返す
    return results

if __name__=="__main__":
    res = worst_quiz()
    print(res)