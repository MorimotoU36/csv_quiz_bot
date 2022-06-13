# -*- coding: utf-8 -*-
import os
import sys
import time
import traceback
import pymysql
import pymysql.cursors

import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
import select_quiz
import add_quiz

sys.path.append(os.path.join(os.path.dirname(__file__), '../module'))
from dbconfig import get_connection, get_file_info
from ini import get_messages_ini

from ut_common import delete_all_quiz_of_file

class TestSelectQuiz(unittest.TestCase):

    # 問題を1つ取ってくるテスト
    def test_select_quiz(self):

        # 入力データ
        input_data = "select_quizテスト1問題,select_quizテスト1答え,select_quizテスト1カテゴリ,select_quizテスト1画像"
        # 使用ファイル番号（テスト用テーブル）
        file_num = 0

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

        # テスト用テーブルのデータ全件削除
        self.assertEqual(delete_all_quiz_of_file(conn,file_num),0)

        # データ追加
        add_quiz.add_quiz(file_num,input_data)

        # データ取得
        response = select_quiz.select_quiz(file_num,1)

        self.assertEqual(response['statusCode'],200)
        result = response['result']
        self.assertEqual(len(result),1)
        self.assertEqual(result[0]['file_num'],0)
        self.assertEqual(result[0]['quiz_num'],1)
        self.assertEqual(result[0]['quiz_sentense'],'select_quizテスト1問題')
        self.assertEqual(result[0]['answer'],'select_quizテスト1答え')
        self.assertEqual(result[0]['clear_count'],0)
        self.assertEqual(result[0]['fail_count'],0)
        self.assertEqual(result[0]['category'],'select_quizテスト1カテゴリ')
        self.assertEqual(result[0]['img_file'],'select_quizテスト1画像')
        self.assertEqual(result[0]['checked'],0)
        self.assertEqual(result[0]['deleted'],0)
        self.assertEqual(result[0]['accuracy_rate'],'0')

        # 終わったらテストデータ削除
        self.assertEqual(delete_all_quiz_of_file(conn,file_num),0)

        # 全て成功したらコミット
        conn.commit()
        conn.close()

    # エラーメッセージのテスト
    def test_config_error(self):

        # データ取得
        response = select_quiz.select_quiz(99999999,1)

        # 取得データ確認
        self.assertEqual(response['statusCode'],400)
        self.assertEqual(response['message'],'Error: ファイル番号が正しくありません')

    # エラーメッセージのテスト２
    def test_data_num_error(self):
        # 入力データ
        input_data = "select_quizテスト1問題,select_quizテスト1答え,select_quizテスト1カテゴリ,select_quizテスト1画像"
        # 使用ファイル番号（テスト用テーブル）
        file_num = 0

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

        # テスト用テーブルのデータ全件削除
        self.assertEqual(delete_all_quiz_of_file(conn,file_num),0)

        # データ追加
        add_quiz.add_quiz(file_num,input_data)

        # データ取得（エラー）
        response = select_quiz.select_quiz(file_num,999999)

        # 取得データ確認
        self.assertEqual(response['statusCode'],500)
        self.assertEqual(response['message'],'Error: 単体テスト用の問題番号は1~1の間で入力してください')

        # 終わったらテストデータ削除
        self.assertEqual(delete_all_quiz_of_file(conn,file_num),0)

        # 全て成功したらコミット
        conn.commit()
        conn.close()

if __name__ == '__main__':
    unittest.main()