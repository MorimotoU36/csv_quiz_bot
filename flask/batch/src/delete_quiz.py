# -*- coding: utf-8 -*-
import os
import sys
import traceback
import pymysql
import pymysql.cursors

sys.path.append(os.path.join(os.path.dirname(__file__), '../module'))
from dbconfig import get_connection, get_file_info
from ini import get_messages_ini

def delete_quiz(file_num,quiz_num):
    """入力データで問題を削除する関数

    Args:
        file_num (int): ファイル番号
        quiz_num (int): 問題番号
        question (str): 問題文
        answer (str): 答えの文
        category (str): カテゴリ
        img_file (str): 画像ファイル名

    Returns:
        [type]: [description]
    """

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
        # 入力内容からSQLを作成して投げる
        # SQLを実行する
        with conn.cursor() as cursor:
            # テーブルに問題を削除しにいく（削除フラグを更新する）
            update_deleteflag = " deleted = 1 "
            sql = "UPDATE quiz SET {0} WHERE file_num = {1} AND quiz_num = {2} ".format(update_deleteflag,file_num,quiz_num)
            cursor.execute(sql)

            result = "Success!! [{0}-{1}]: deleted!".format(nickname,str(quiz_num))

        #全て成功したらコミット
        conn.commit()
        conn.close()

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

    # 結果(文字列)を返す
    return {
        "statusCode": 200,
        "result": result
    }


if __name__=="__main__":
    print("delete_quiz!!")