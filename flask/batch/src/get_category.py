# -*- coding: utf-8 -*-
import os
import sys
import traceback
import pymysql
import pymysql.cursors

sys.path.append(os.path.join(os.path.dirname(__file__), '../module'))
from dbconfig import get_connection
from ini import get_table_list

def get_category(file_num):
    """ファイル番号からカテゴリを取得する関数

    Args:
        file_num (int): ファイル番号

        Returns:
            result [JSON]: 取得したカテゴリのリスト
    """

    # 設定ファイルを呼び出してファイル番号からテーブル名を取得
    # (変なファイル番号ならエラー終了)
    try:
        table_list = get_table_list()
        table = table_list[file_num]['name']
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

    # # SQLを作成して投げる
    with conn.cursor() as cursor:
        # 検索語句がカテゴリに含まれる
        # SQLを実行する
        sql_statement = "SELECT DISTINCT category FROM {0} ".format(table)
        cursor.execute(sql_statement)

        # MySQLから帰ってきた結果を受け取る
        # Select結果を取り出す
        results = cursor.fetchall()

        categories = set([])
        for ri in results:
            categories = categories | set(list(ri['category'].split(':')))

    # 結果をJSONに変形して返す
    return {
        "statusCode": 200,
        "result": list(categories)
    }

if __name__=="__main__":
    res = get_category(0)
    print(res)