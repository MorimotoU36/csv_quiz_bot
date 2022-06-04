# -*- coding: utf-8 -*-
import os
import sys
import traceback
import pymysql
import pymysql.cursors

sys.path.append(os.path.join(os.path.dirname(__file__), '../module'))
from dbconfig import get_connection
from ini import get_table_list

def select_quiz(file_num,quiz_num):
    """ファイル番号、問題番号から問題を取得する関数

    Args:
        file_num (int): ファイル番号
        quiz_num (int): 問題番号

        Returns:
            result (JSON): 取得した問題
    """

    # 設定ファイルを呼び出してファイル番号からテーブル名を取得
    # (変なファイル番号ならエラー終了)
    try:
        table_list = get_table_list()
        table = table_list[file_num]['name']
        view = table+"_view"
        nickname = table_list[file_num]['nickname']
    except IndexError:
        return {
            "statusCode": 500,
            "message": 'Error: ファイル番号が正しくありません'
        }

    # MySQL への接続を確立する
    try:
        conn = get_connection()
    except Exception as e:
        return {
            "statusCode": 500,
            "message": 'Error: DB接続時にエラーが発生しました',
            "traceback": traceback.format_exc()
        }

    # テーブル名と問題番号からSQLを作成して投げる
    # (問題番号が範囲外なら終了)
    # SQLを実行する
    with conn.cursor() as cursor:
        # 指定したテーブルの件数を調べる
        sql = "SELECT count(*) FROM {0}".format(table)
        cursor.execute(sql)
        results = cursor.fetchall()
        for r in results:
            count = r['count(*)']

        # 問題番号が範囲外なら終了
        if(quiz_num < 1 or count < quiz_num):
            return {
                "statusCode": 500,
                "message": 'Error: {0}の問題番号は1~{1}の間で入力してください'.format(nickname,count)
            }

        sql = "SELECT quiz_num, quiz_sentense, answer, clear_count, fail_count, category, img_file, checked, deleted, accuracy_rate FROM {0} WHERE quiz_num = {1}".format(view,quiz_num)
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