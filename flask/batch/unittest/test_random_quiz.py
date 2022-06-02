# -*- coding: utf-8 -*-
import os
import sys
import time
import traceback
import pymysql
import pymysql.cursors

import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
import random_quiz
import add_quiz

sys.path.append(os.path.join(os.path.dirname(__file__), '../module'))
from dbconfig import get_connection
from ini import get_table_list

class TestSelectQuiz(unittest.TestCase):

    # 問題を1つ取ってくるテスト
    def test_random_quiz(self):

        # 入力データ
        input_data = "\n".join(["random_quizテスト1問題,random_quizテスト1答え,random_quizテスト1カテゴリ,random_quizテスト1画像"
                                ,"random_quizテスト2問題,random_quizテスト2答え,random_quizテスト2カテゴリ,random_quizテスト2画像"
                                ,"random_quizテスト3問題,random_quizテスト3答え,random_quizテスト3カテゴリ,random_quizテスト3画像"
                                ,"random_quizテスト4問題,random_quizテスト4答え,random_quizテスト4カテゴリ,random_quizテスト4画像"
                                ,"random_quizテスト5問題,random_quizテスト5答え,random_quizテスト5カテゴリ,random_quizテスト5画像"])
        # 使用ファイル番号（テスト用テーブル）
        file_num = 0

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
        response = random_quiz.random_quiz(file_num=file_num)
        self.assertEqual(response['statusCode'],200)
        result = response['result']
        self.assertEqual(len(result),1)
        self.assertTrue(1 <= result[0]['quiz_num'] and result[0]['quiz_num'] <= 5)
        self.assertEqual(result[0]['quiz_sentense'][:11],'random_quiz')
        self.assertEqual(result[0]['answer'][:11],'random_quiz')
        self.assertEqual(result[0]['clear_count'],0)
        self.assertEqual(result[0]['fail_count'],0)
        self.assertEqual(result[0]['category'][:11],'random_quiz')
        self.assertEqual(result[0]['img_file'][:11],'random_quiz')
        self.assertEqual(result[0]['checked'],0)
        self.assertEqual(result[0]['deleted'],0)
        self.assertEqual(result[0]['accuracy_rate'],'0')

        with conn.cursor() as cursor:
            # 終わったらテストデータ削除
            sql = "DELETE FROM {0} ".format(table)
            cursor.execute(sql)

        # 全て成功したらコミット
        conn.commit()
        conn.close()

if __name__ == '__main__':
    unittest.main()