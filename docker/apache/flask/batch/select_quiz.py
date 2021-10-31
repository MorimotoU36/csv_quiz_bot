# -*- coding: utf-8 -*-

def select_quiz(file_num,quiz_num,image_flag):
    """ファイル番号、問題番号、イメージ取得フラグから問題を取得する関数

    Args:
        file_num (int): ファイル番号
        quiz_num (int): 問題番号
        image_flag (bool): イメージ取得フラグ
    """

    # 設定ファイルを呼び出してファイル番号からテーブル名を取得
    # (変なファイル番号ならエラー終了)

    # MySQL への接続を確立する

    # テーブル名と問題番号からSQLを作成して投げる
    # (問題番号が範囲外なら終了)

    # MySQLから帰ってきた結果を受け取る

    # 結果をJSONに変形して返す

