# -*- coding: utf-8 -*-
import os
import sys
import traceback
import pymysql
import pymysql.cursors

sys.path.append(os.path.join(os.path.dirname(__file__), '../module'))
from dbconfig import get_connection
from ini import get_table_list

from add_quiz import add_quiz

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


    try:
        # 入力内容からSQLを作成して投げる
        # SQLを実行する
        with conn.cursor() as cursor:
            # テーブルに問題を削除しにいく（削除フラグを更新する）
            update_deleteflag = " deleted = 1 "
            sql = "UPDATE {0} SET {1} WHERE quiz_num = {2} ".format(table,update_deleteflag,quiz_num)
            print(sql)
            cursor.execute(sql)

            result = "Success!! [{0}-{1}]: deleted!".format(nickname,str(quiz_num))

        #全て成功したらコミット
        conn.commit()
        conn.close()

    # DB操作失敗時はロールバック
    except Exception as e:
        message = 'Error: DB操作時にエラーが発生しました '
        try:
            conn.rollback()
        except:
            message += '( ロールバックにも失敗しました )'
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

    # 削除用ダミーデータ追加
    add_ress = add_quiz(2,"削除用テストデータ１の問題,削除用テストデータ１の答え,削除用テストデータ１のカテゴリ,削除用テストデータ１のimgfile")
    add_ress2 = add_quiz(2,"削除用テストデータ２の問題,削除用テストデータ２の答え,削除用テストデータ２のカテゴリ,削除用テストデータ２のimgfile")
    print(add_ress)
    print(add_ress2)

    # ダミーデータ1つ削除
    res = delete_quiz(2,98)
    print(res)