# -*- coding: utf-8 -*-
import os
import sys
import traceback
import pymysql
import pymysql.cursors

sys.path.append(os.path.join(os.path.dirname(__file__), '../module'))
from dbconfig import get_connection
from ini import get_table_list

def select_quiz(file_num,quiz_num,image_flag):
    """ファイル番号、問題番号、イメージ取得フラグから問題を取得する関数

    Args:
        file_num (int): ファイル番号
        quiz_num (int): 問題番号
        image_flag (bool): イメージ取得フラグ

        Returns:
            result (JSON): 取得した問題
    """

    # 設定ファイルを呼び出してファイル番号からテーブル名を取得
    # (変なファイル番号ならエラー終了)
    try:
        table_list = get_table_list()
        table = table_list[file_num]['name']
        nickname = table_list[file_num]['nickname']
    except IndexError:
        print('Error: ファイル番号が正しくありません')
        sys.exit()

    # MySQL への接続を確立する
    try:
        conn = get_connection()
    except Exception as e:
        print('Error: DB接続時にエラーが発生しました')
        print(traceback.format_exc())
        sys.exit()

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
            print('Error: {0}の問題番号は1~{1}の間で入力してください'.format(nickname,count))
            sys.exit()

        sql = "SELECT quiz_num, quiz_sentense, answer, clear_count, fail_count, category, img_file FROM {0} WHERE quiz_num = {1}".format(table,quiz_num)
        cursor.execute(sql)

        # MySQLから帰ってきた結果を受け取る
        # Select結果を取り出す
        results = cursor.fetchall()

    # 結果をJSONに変形して返す
    return results[0]

if __name__=="__main__":
    res = select_quiz(0,100,False)
    print(res)