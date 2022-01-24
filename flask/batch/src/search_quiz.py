# -*- coding: utf-8 -*-
import os
import sys
import traceback
import pymysql
import pymysql.cursors

sys.path.append(os.path.join(os.path.dirname(__file__), '../module'))
from dbconfig import get_connection
from ini import get_table_list

def search_quiz(query,file_num,cond,category,checked=False):
    """検索語句から問題を取得する関数

    Args:
        query (str): 検索語句
        file_num (int): ファイル番号
        cond(JSON): 検索条件のオプション
        category (str): カテゴリ
        checked (bool, optional): チェックした問題だけから出題するかのフラグ. Defaults to False.

        Returns:
            result [JSON]: 取得した問題のリスト
    """

    # 設定ファイルを呼び出してファイル番号からテーブル名を取得
    # (変なファイル番号ならエラー終了)
    try:
        table_list = get_table_list()
        table = table_list[file_num]['name']
        nickname = table_list[file_num]['nickname']
        cond_question = cond.get('question',False)
        cond_answer = cond.get('answer',False)
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
    with conn.cursor() as cursor:
        # 検索語句が問題文または解答文に含まれる
        # SQLを実行する
        sql_statement = "SELECT quiz_num, quiz_sentense, answer, clear_count, fail_count, category, img_file, checked FROM {0} ".format(table,query)
        sql_statement += " WHERE "
        where_statement=[]
        if(not cond_question and not cond_answer):
            where_statement.append(" (quiz_sentense LIKE '%{0}%' OR answer LIKE '%{0}%') ".format(query))
        if(cond_question):
            # 問題にチェックあったときは語句が含まれている問題文を検索
            where_statement.append(" quiz_sentense LIKE '%{0}%' ".format(query))
        if(cond_answer):
            # 答えにチェックあったときは語句が含まれている解答文を検索
            where_statement.append(" answer LIKE '%{0}%' ".format(query))
        if(category != ""):
            # カテゴリを指定して検索
            where_statement.append(" category LIKE '%{0}%' ".format(category))
        if(checked):
            # checked=True の時はチェック済みの問題のみを検索
            where_statement.append(" checked != 0 ")

        sql_statement += ' AND '.join(where_statement)

        cursor.execute(sql_statement)

        # MySQLから帰ってきた結果を受け取る
        # Select結果を取り出す
        results = cursor.fetchall()

    # 結果をJSONに変形して返す
    return {
        "statusCode": 200,
        "result": results
    }

if __name__=="__main__":
    res = search_quiz('VPC',0)
    print(res)