# -*- coding: utf-8 -*-
import os
import sys
import random
import traceback
import pymysql
import pymysql.cursors

sys.path.append(os.path.join(os.path.dirname(__file__), '../module'))
from dbconfig import get_connection, get_file_info
from ini import get_messages_ini

def answer_input(file_num,quiz_num,clear):
    """正解不正解データを受け取ってデータを登録する

    Args:
        answer_data (JSON): 解答データのJSON
            解答データは
            {
                "file_num": ファイル番号
                "quiz_num": 問題番号
                "clear": 正解ならTrue、不正解ならFalse
            }

    Returns:
        str: レコードのSQL、実行結果
    """

    # 結果
    result = ""

    # メッセージ設定ファイルを呼び出す
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

    # ファイル番号からテーブル名を取得
    table_info = get_file_info(conn,file_num)
    if(table_info['statusCode'] == 200):
        nickname = table_info['result']['file_nickname']
    else:
        return {
            "statusCode": 400,
            "message": messages['ERR_0001']
        }

        
    try:
        # 設定ファイルを呼び出してファイル番号からテーブル名を取得
        # (変なファイル番号ならエラー終了)
        file_num = int(file_num)
        quiz_num = int(quiz_num)
        isclear = bool(clear)
    
        # テーブル名からSQLを作成して投げる
        with conn.cursor() as cursor:
            # 指定した問題の正解(不正解)数を取得する
            get_column_name = "clear_count" if isclear else "fail_count"
            sql = "SELECT " + get_column_name + " FROM quiz WHERE file_num = {0} AND quiz_num = {1}".format(file_num,quiz_num)
            cursor.execute(sql)
            results = cursor.fetchall()
            num = int(results[0][get_column_name])

            # 正解(不正解)数+1
            num += 1

            # SQL作成して更新する
            sql = "UPDATE quiz SET {0} = {1} WHERE file_num = {2} AND quiz_num = {3}".format(get_column_name,num,file_num,quiz_num)
            cursor.execute(sql)

            # 結果を格納する
            result = "[" + nickname + "-" + str(quiz_num) + "]:" + ("正解" if isclear else "不正解") + " 登録OK"

        #全て成功したらコミット
        conn.commit()
        conn.close()

    except IndexError:
        return {
            "statusCode": 500,
            "message": messages['ERR_0001']
        }
    # DB操作失敗時はロールバック
    except Exception as e:
        message = messages['ERR_0004']
        try:
            conn.rollback()
        except:
            message = messages['ERR_0005']
        finally:
            return {
                "statusCode": 500,
                "message": message,
                "traceback": traceback.format_exc()
            }

    # 結果を返す
    return {
        "statusCode": 200,
        "result": result
    }

if __name__=="__main__":
    print("answer_inputters")