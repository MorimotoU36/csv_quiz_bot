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

def random_quiz(file_num=-1,rate=100,category="",checked=False):
    """問題を１問、ランダムに取得するAPI

    Args:
        file_num (int, optional): ファイル番号. Defaults to -1.
        rate (float, optional): 取得する問題の正解率の最大値. Defaults to 100., 0 ~ 100
        category (str, optional): 取得する問題のカテゴリ Defaults to ''
        checked (bool, optional): チェックした問題だけから出題するかのフラグ. Defaults to False.

    Returns:
        result (JSON): ランダムに取得した問題
    """

    # 設定ファイルを呼び出してファイル番号からテーブル名を取得
    # (変なファイル番号の時はランダムに選ぶ)
    table_list = get_table_list()
    if(file_num < 0 or len(table_list) <= file_num):
        file_num = random.randint(0,len(table_list)-1)
    table = table_list[file_num]['name']
    view = table+"_view"
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
    
    # WHERE文
    where_statement = []

    # rateによる条件追加
    where_statement.append(" accuracy_rate <= {0} ".format(rate))

    # カテゴリによる条件追加
    if(len(category)>0):
        where_statement.append(" category LIKE '%" + category + "%' ")
    if(checked):
        where_statement.append(" checked != 0 ")
    
    # WHERE文を作る
    if(len(where_statement) > 0):
        where_statement = ' WHERE ' + ' AND '.join(where_statement)
    else:
        where_statement = ''
    
    # テーブル名からSQLを作成して投げる
    with conn.cursor() as cursor:
        # SQL作成して問題を取得する。結果のうちランダムに1つ取得する
        sql = "SELECT quiz_num, quiz_sentense, answer, clear_count, fail_count, category, img_file, checked, accuracy_rate FROM {0} {1} ORDER BY RAND() LIMIT 1".format(view,where_statement)
        cursor.execute(sql)

        # MySQLから帰ってきた結果を受け取る
        # Select結果を取り出す
        results = cursor.fetchall()
        # accuracy_rateはstr型にする(API)
        for ri in results:
            ri["accuracy_rate"] = str(ri["accuracy_rate"])

    # 結果をJSONに変形して返す
    return {
        "statusCode": 200,
        "result": results
    }

if __name__=="__main__":
    res = random_quiz(file_num=0,category='')
    print(res)