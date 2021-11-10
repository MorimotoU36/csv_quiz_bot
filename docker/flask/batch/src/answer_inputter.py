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

def answer_input(answer_data):
    """正解不正解データの配列を受け取ってデータを登録する

    Args:
        answer_data ([JSON]): 解答データのJSON配列
            解答データは
            {
                "file_num": ファイル番号
                "quiz_num": 問題番号
                "clear": 正解ならTrue、不正解ならFalse
            }

    Returns:
        [str]: 各レコードのSQL、実行結果
    """

    # 結果
    result = []

    # 設定ファイルを呼び出す
    table_list = get_table_list()

    # MySQL への接続を確立する
    try:
        conn = get_connection()
    except Exception as e:
        print('Error: DB接続時にエラーが発生しました')
        print(traceback.format_exc())
        sys.exit()
        
    try:
        # 入力データ1つずつ処理する
        for answer in answer_data:

            # 設定ファイルを呼び出してファイル番号からテーブル名を取得
            # (変なファイル番号ならエラー終了)
            file_num = int(answer['file_num'])
            quiz_num = int(answer['quiz_num'])
            isclear = bool(answer['clear'])
            table = table_list[file_num]['name']
            nickname = table_list[file_num]['nickname']
        
            # テーブル名からSQLを作成して投げる
            with conn.cursor() as cursor:
                # 指定した問題の正解(不正解)数を取得する
                get_column_name = "clear_count" if isclear else "fail_count"
                sql = "SELECT " + get_column_name + " FROM {0} where quiz_num = {1}".format(table,quiz_num)
                cursor.execute(sql)
                results = cursor.fetchall()
                num = int(results[0][get_column_name])

                # 正解(不正解)数+1
                num += 1

                # SQL作成して更新する
                sql = "UPDATE {0} SET {1} = {2} WHERE quiz_num = {3}".format(table,get_column_name,num,quiz_num)
                cursor.execute(sql)

                # SQLとUPDATE結果を格納する
                result.append(sql + ":" + "OK")
        else:
            #全て成功したらコミット
            conn.commit()
            conn.close()

    # DB操作失敗時はロールバック
    except Exception as e:
        print("Error. DB操作時にエラーが発生しました")
        print(traceback.format_exc())
        try:
            conn.rollback()
        except:
            print("rollback failed")

    # 結果をJSONに変形して返す
    return result

if __name__=="__main__":
    input = [
        {
            "file_num": 0,
            "quiz_num": 1,
            "clear": "true"
        },
        {
            "file_num": 0,
            "quiz_num": 2,
            "clear": False
        }
    ]
    res = answer_input(input)
    print(res)