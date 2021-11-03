# -*- coding: utf-8 -*-
import os
import sys
import traceback
import pymysql
import pymysql.cursors

sys.path.append(os.path.join(os.path.dirname(__file__), '../module'))
from dbconfig import get_connection
from ini import get_table_list

def random_quiz(file_num=-1,image=True,rate=100.0):

    # 設定ファイルを呼び出してファイル番号からテーブル名を取得
    # (変なファイル番号の時はランダムに選ぶ)

    # MySQL への接続を確立する

    # テーブル名からSQLを作成して投げる
    # 指定したテーブルの件数を調べる
    # 問題番号をランダムで選ぶ

    # SQL作って投げて問題を取得する

    # 結果をJSONに変形して返す
