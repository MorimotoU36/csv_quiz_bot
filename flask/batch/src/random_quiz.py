# -*- coding: utf-8 -*-
import os
import sys
import random
import traceback
import pymysql
import pymysql.cursors

sys.path.append(os.path.join(os.path.dirname(__file__), '../module'))
from dbconfig import get_connection
from ini import get_table_list, get_messages_ini

def random_quiz(file_num=-1,min_rate=0,max_rate=100,category="",checked=False):
    """問題を１問、ランダムに取得するAPI

    Args:
        file_num (int, optional): ファイル番号. Defaults to -1.
        min_rate (float, optional): 取得する問題の正解率の最小値. Defaults to   0., 0 ~ 100
        max_rate (float, optional): 取得する問題の正解率の最大値. Defaults to 100., 0 ~ 100
        category (str, optional): 取得する問題のカテゴリ Defaults to ''
        checked (bool, optional): チェックした問題だけから出題するかのフラグ. Defaults to False.

    Returns:
        result (JSON): ランダムに取得した問題
    """

    # 設定ファイルを呼び出してファイル番号からテーブル名を取得
    # (変なファイル番号の時はランダムに選ぶ)
    messages = get_messages_ini()
    table_list = get_table_list()
    try:
        if(file_num < 0 or len(table_list) <= file_num):
            file_num = random.randint(0,len(table_list)-1)
        table = table_list[file_num]['name']
        view = table+"_view"
        nickname = table_list[file_num]['nickname']
    except IndexError:
        return {
            "statusCode": 500,
            "message": messages['ERR_0001']
        }

    # min_rate > max_rateの場合はエラー終了
    if(min_rate > max_rate):
        return {
            "statusCode": 400,
            "message": messages['ERR_0011'].format(min_rate,max_rate)
        }

    # MySQL への接続を確立する
    try:
        conn = get_connection()
    except Exception as e:
        return {
            "statusCode": 500,
            "message": messages['ERR_0002'],
            "traceback": traceback.format_exc()
        }
    
    # WHERE文
    where_statement = []

    # rateによる条件追加(正解数・不正解数0回の時は正解率NULLになるが、それは正解率指定に関係なく出させる事にする。)
    where_statement.append(" ( accuracy_rate IS NULL OR ( {0} <= accuracy_rate AND accuracy_rate <= {1} ) )".format(min_rate,max_rate))

    # 削除済問題を取らない条件追加
    where_statement.append(" deleted != 1 ")

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
        sql = "SELECT quiz_num, quiz_sentense, answer, clear_count, fail_count, category, img_file, checked, deleted, accuracy_rate FROM {0} {1} ORDER BY RAND() LIMIT 1".format(view,where_statement)
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

if __name__=="__main__":
    print("random_quiz!")