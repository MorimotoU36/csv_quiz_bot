# -*- coding: utf-8 -*-
import os
import sys
import traceback
import pymysql
import pymysql.cursors

sys.path.append(os.path.join(os.path.dirname(__file__), '../module'))
from dbconfig import get_connection
from ini import get_table_list

def edit_quiz(file_num,quiz_num,question,answer,category,img_file):
    """入力データで問題を編集する関数

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

    # 入力内容確認
    if (question is None or len(question.strip())==0) and (answer is None or len(answer.strip())==0) and (category is None or len(category.strip())==0) and (img_file is None or len(img_file.strip())==0):
        return {
            "statusCode": 500,
            "message": 'Error: 入力内容がありません'
        }

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
            # テーブルに入力内容を更新する
            update_question = "" if question is None or len(question.strip())==0 else " quiz_sentense = '{0}', ".format(question)
            update_answer   = "" if answer is None or len(answer.strip())==0 else " answer = '{0}', ".format(answer)
            update_category = "" if category is None or len(category.strip())==0 else " category = '{0}', ".format(category)
            update_img_file = " img_file = '' " if img_file is None else " img_file = '{0}' ".format(img_file)
            sql = "UPDATE {0} SET {1} {2} {3} {4} WHERE quiz_num = {5} ".format(table,update_question,update_answer,update_category,update_img_file,quiz_num)
            print(sql)
            cursor.execute(sql)

            result = "Success!! [{0}-{1}]:{2},{3},{4},{5}".format(nickname,str(quiz_num),question,answer,category,img_file)

        #全て成功したらコミット
        conn.commit()
        conn.close()

    # DB操作失敗時はロールバック
    except Exception as e:
        message = 'Error: DB接続時にエラーが発生しました '
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
    res = edit_quiz(2,99,"ques1","ans2","cat3","img4")
    print(res)