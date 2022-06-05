# -*- coding: utf-8 -*-
import os
import sys
import time
import traceback
import pymysql
import pymysql.cursors

import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
import search_quiz
import add_quiz

sys.path.append(os.path.join(os.path.dirname(__file__), '../module'))
from dbconfig import get_connection
from ini import get_table_list, get_messages_ini

class TestSearchQuiz(unittest.TestCase):

    # 問題を1つ取ってくるテスト
    def test_search_quiz(self):

        # 入力データ
        input_data = "\n".join(["search_quizテスト1問題,search_quizテスト1答え,search_quizテスト1カテゴリ,search_quizテスト1画像"
                                ,"search_quizテスト2問題,search_quizテスト2答え,search_quizテスト2カテゴリ,search_quizテスト2画像"
                                ,"search_quizテスト3問題,search_quizテスト3答え,search_quizテスト3カテゴリ,search_quizテスト3画像"
                                ,"search_quizテスト4問題,search_quizテスト4答え,search_quizテスト4カテゴリ,search_quizテスト4画像"
                                ,"search_quizテスト5問題,search_quizテスト5答え,search_quizテスト5カテゴリ,search_quizテスト5画像"])
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

        # データ取得
        response = search_quiz.search_quiz('search_quizテスト1',file_num)
        self.assertEqual(response['statusCode'],200)
        result = response['result']
        self.assertEqual(len(result),1)
        self.assertEqual(result[0]['quiz_num'],1)
        self.assertEqual(result[0]['quiz_sentense'],'search_quizテスト1問題')
        self.assertEqual(result[0]['answer'],'search_quizテスト1答え')
        self.assertEqual(result[0]['clear_count'],0)
        self.assertEqual(result[0]['fail_count'],0)
        self.assertEqual(result[0]['category'],'search_quizテスト1カテゴリ')
        self.assertEqual(result[0]['img_file'],'search_quizテスト1画像')
        self.assertEqual(result[0]['checked'],0)
        self.assertEqual(result[0]['deleted'],0)
        self.assertEqual(result[0]['accuracy_rate'],'None')

        with conn.cursor() as cursor:
            # 終わったらテストデータ削除
            sql = "DELETE FROM {0} ".format(table)
            cursor.execute(sql)

        # 全て成功したらコミット
        conn.commit()
        conn.close()

if __name__ == '__main__':
    unittest.main()