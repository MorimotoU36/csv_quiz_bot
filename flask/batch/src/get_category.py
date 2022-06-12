# -*- coding: utf-8 -*-
import os
import sys
import traceback
import pymysql
import pymysql.cursors

sys.path.append(os.path.join(os.path.dirname(__file__), '../module'))
from dbconfig import get_connection
from ini import get_messages_ini

def get_category(file_num):
    """ファイル番号からカテゴリを取得する関数

    Args:
        file_num (int): ファイル番号

        Returns:
            result [JSON]: 取得したカテゴリのリスト
    """

    # 設定ファイルを呼び出す
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

    # # SQLを作成して投げる
    with conn.cursor() as cursor:
        # 検索語句がカテゴリに含まれる
        # SQLを実行する
        sql_statement = "SELECT DISTINCT category FROM quiz WHERE file_num = {0} AND deleted != 1 ".format(file_num)
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
    print("get_category!")