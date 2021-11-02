# -*- coding: utf-8 -*-
import os
import sys
import traceback

sys.path.append(os.path.join(os.path.dirname(__file__), '../module'))
from dbconfig import get_connection
from ini import get_table_list

def select_quiz(file_num,quiz_num,image_flag):
    """ファイル番号、問題番号、イメージ取得フラグから問題を取得する関数

    Args:
        file_num (int): ファイル番号
        quiz_num (int): 問題番号
        image_flag (bool): イメージ取得フラグ
    """

    # 設定ファイルを呼び出してファイル番号からテーブル名を取得
    # (変なファイル番号ならエラー終了)
    try:
        table_list = get_table_list()
        table = table_list[file_num]['name']
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

    # MySQLから帰ってきた結果を受け取る

    # 結果をJSONに変形して返す

if __name__=="__main__":
    select_quiz(1,1,False)