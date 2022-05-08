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

def worst_quiz(file_num=-1,category=None,checked=False):
    """最低正解率の問題を取得

    Args:
        file_num (int, optional): ファイル番号. Defaults to -1.
        category (str, optional): カテゴリ. Defaults to None.
        checked (bool, optional): チェックした問題だけから出題するかのフラグ. Defaults to False.

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
    try:
        with conn.cursor() as cursor:
            # 指定したテーブルの正解率が最も低い問題を調べる
            # カテゴリが指定されている場合は条件文を追加する
            where_statement = []
            if(category is not None):
                where_statement.append(" category LIKE '%"+category+"%' ")
            if(checked):
                where_statement.append(" checked != 0 ")
            
            if(len(where_statement) > 0):
                where_statement = ' WHERE ' + ' AND '.join(where_statement)
            else:
                where_statement = ''

            sql = "SELECT quiz_num FROM {0} ".format(view) + where_statement + " ORDER BY accuracy_rate LIMIT 1"
            print(sql)
            cursor.execute(sql)
            results = cursor.fetchall()

            # 取得結果0件ならば終了
            if(len(results) <= 0):
                return {
                    "statusCode": 200,
                    "result": results
                }                

            quiz_id = results[0]['quiz_num']

            # SQL作成して問題を取得する
            sql = "SELECT quiz_num, quiz_sentense, answer, clear_count, fail_count, category, img_file, checked, accuracy_rate FROM {0} WHERE quiz_num = {1}".format(view,quiz_id)
            print(sql)
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
            "message": 'Error: DB操作時にエラーが発生しました',
            "traceback": traceback.format_exc()
        }

if __name__=="__main__":
    res = worst_quiz(file_num=0,category="SAA",checked=True)
    print(res)