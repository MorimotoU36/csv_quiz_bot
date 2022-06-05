# -*- coding: utf-8 -*-
import os
import sys
import time
import traceback
import pymysql
import pymysql.cursors

import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
import answer_inputter
import add_quiz

sys.path.append(os.path.join(os.path.dirname(__file__), '../module'))
from dbconfig import get_connection
from ini import get_table_list, get_messages_ini

class TestAnswerInputter(unittest.TestCase):

    # 問題を1つ取ってくるテスト
    def test_answer_inputter(self):

        # 入力データ
        input_data = "answer_inputterテスト1問題,answer_inputterテスト1答え,answer_inputterテスト1カテゴリ,answer_inputterテスト1画像"
        # 使用ファイル番号（テスト用テーブル）
        file_num = 0

        # 設定ファイルを呼び出してファイル番号からテーブル名を取得
        # (変なファイル番号ならエラー終了)
        messages = get_messages_ini()
        table_list = get_table_list()
        try:
            table = table_list[file_num]['name']
            nickname = table_list[file_num]['nickname']
        except IndexError:
            return {
                "statusCode": 500,
                "message": messages['ERR_0001']
            }

        # MySQL への接続を確立する
        try:
            conn = get_connection()
        except Exception as e:
            return {
                "statusCode": 500,
                "message": messages['ERR_0002'],
                "traceback": traceback.format_exc()
            }

        with conn.cursor() as cursor:
            # テスト用テーブルのデータ全件削除
            sql = "DELETE FROM {0} ".format(table)
            cursor.execute(sql)
            # 全件削除されたか確認
            sql = "SELECT count(*) FROM {0} ".format(table)
            cursor.execute(sql)
            sql_results = cursor.fetchall()
            self.assertEqual(sql_results[0]['count(*)'],0)
            # コミット
            conn.commit()

        # データ追加
        add_quiz.add_quiz(file_num,input_data)

        # 正解登録
        answer_inputter.answer_input(0,1,True)

        # データ確認
        with conn.cursor() as cursor:
            # 全件削除されたか確認
            sql = "SELECT * FROM {0} ".format(table)
            cursor.execute(sql)
            results = cursor.fetchall()
            self.assertEqual(len(results),1)
            self.assertEqual(results[0]['quiz_num'],1)
            self.assertEqual(results[0]['quiz_sentense'],'answer_inputterテスト1問題')
            self.assertEqual(results[0]['answer'],'answer_inputterテスト1答え')
            self.assertEqual(results[0]['clear_count'],1)
            self.assertEqual(results[0]['fail_count'],0)
            self.assertEqual(results[0]['category'],'answer_inputterテスト1カテゴリ')
            self.assertEqual(results[0]['img_file'],'answer_inputterテスト1画像')
            self.assertEqual(results[0]['checked'],0)
            self.assertEqual(results[0]['deleted'],0)
            # コミット
            conn.commit()

        # 不正解登録
        answer_inputter.answer_input(0,1,False)

        # データ確認
        with conn.cursor() as cursor:
            # 全件削除されたか確認
            sql = "SELECT * FROM {0} ".format(table)
            cursor.execute(sql)
            results = cursor.fetchall()
            self.assertEqual(len(results),1)
            self.assertEqual(results[0]['quiz_num'],1)
            self.assertEqual(results[0]['quiz_sentense'],'answer_inputterテスト1問題')
            self.assertEqual(results[0]['answer'],'answer_inputterテスト1答え')
            self.assertEqual(results[0]['clear_count'],1)
            self.assertEqual(results[0]['fail_count'],1)
            self.assertEqual(results[0]['category'],'answer_inputterテスト1カテゴリ')
            self.assertEqual(results[0]['img_file'],'answer_inputterテスト1画像')
            self.assertEqual(results[0]['checked'],0)
            self.assertEqual(results[0]['deleted'],0)

        with conn.cursor() as cursor:
            # 終わったらテストデータ削除
            sql = "DELETE FROM {0} ".format(table)
            cursor.execute(sql)

        # 全て成功したらコミット
        conn.commit()
        conn.close()

if __name__ == '__main__':
    unittest.main()