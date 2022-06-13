# -*- coding: utf-8 -*-
import os
import sys
import traceback
import pymysql
import pymysql.cursors

sys.path.append(os.path.join(os.path.dirname(__file__), '../module'))
from dbconfig import get_connection, get_file_info
from ini import get_messages_ini

def search_quiz(query,file_num,cond={},category="",rate=100,checked=False):
    """検索語句から問題を取得する関数

    Args:
        query (str): 検索語句
        file_num (int): ファイル番号
        cond(JSON, optional): 検索条件のオプション
        category (str, optional): カテゴリ
        rate (float, optional): 取得する問題の正解率の最大値. Defaults to 1.0., 0.0 ~ 1.0
        checked (bool, optional): チェックした問題だけから出題するかのフラグ. Defaults to False.

        Returns:
            result [JSON]: 取得した問題のリスト
    """

    cond_question = cond.get('question',False)
    cond_answer = cond.get('answer',False)

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

    # テーブル名と問題番号からSQLを作成して投げる
    with conn.cursor() as cursor:
        # 検索語句が問題文または解答文に含まれる
        # SQLを実行する
        sql_statement = "SELECT file_num, quiz_num, quiz_sentense, answer, clear_count, fail_count, category, img_file, checked, deleted, accuracy_rate FROM quiz_view "
        sql_statement += " WHERE "
        where_statement=[" file_num = {0} ".format(file_num)]

        # 削除済の問題は取らないように設定
        where_statement.append(" deleted != 1 ")

        # rateによる条件追加(NULLも)
        where_statement.append(" ( accuracy_rate <= {0} or accuracy_rate is null ) ".format(rate))

        # 入力語句による条件追加((問題・解答両方)
        if(not cond_question and not cond_answer):
            where_statement.append(" (quiz_sentense LIKE '%{0}%' OR answer LIKE '%{0}%') ".format(query))

        # 入力語句による問題文の検索
        if(cond_question):
            # 問題にチェックあったときは語句が含まれている問題文を検索
            where_statement.append(" quiz_sentense LIKE '%{0}%' ".format(query))

        # 入力語句による解答文の検索
        if(cond_answer):
            # 答えにチェックあったときは語句が含まれている解答文を検索
            where_statement.append(" answer LIKE '%{0}%' ".format(query))

        # カテゴリによる検索
        if(category != ""):
            # カテゴリを指定して検索
            where_statement.append(" category LIKE '%{0}%' ".format(category))

        # チェック有の検索
        if(checked):
            # checked=True の時はチェック済みの問題のみを検索
            where_statement.append(" checked != 0 ")

        sql_statement += ' AND '.join(where_statement)

        cursor.execute(sql_statement)

        # MySQLから帰ってきた結果を受け取る
        # Select結果を取り出す
        results = cursor.fetchall()

        # accuracy_rateはstr型にする(API)
        for ri in results:
            ri["accuracy_rate"] = str(ri["accuracy_rate"])


    # 結果をJSONに変形して返す
    return {
        "statusCode": 200,
        "result": results
    }

if __name__=="__main__":
    print("search_quiz!")