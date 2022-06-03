# -*- coding: utf-8 -*-
import os
import sys
import time
import traceback
import pymysql
import pymysql.cursors

import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
import worst_quiz
import add_quiz

sys.path.append(os.path.join(os.path.dirname(__file__), '../module'))
from dbconfig import get_connection
from ini import get_table_list

class TestWorstQuiz(unittest.TestCase):

    # 問題を1つ取ってくるテスト
    def test_worst_quiz(self):

        # 入力データ
        input_data = "\n".join(["worst_quizテスト1問題,worst_quizテスト1答え,worst_quizテスト1カテゴリ,worst_quizテスト1画像"
                                ,"worst_quizテスト2問題,worst_quizテスト2答え,worst_quizテスト2カテゴリ,worst_quizテスト2画像"
                                ,"worst_quizテスト3問題,worst_quizテスト3答え,worst_quizテスト3カテゴリ,worst_quizテスト3画像"
                                ,"worst_quizテスト4問題,worst_quizテスト4答え,worst_quizテスト4カテゴリ,worst_quizテスト4画像"
                                ,"worst_quizテスト5問題,worst_quizテスト5答え,worst_quizテスト5カテゴリ,worst_quizテスト5画像"])
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

        with conn.cursor() as cursor:
            # 正解率操作
            sql = "UPDATE {0} SET clear_count = {1}, fail_count = {2} WHERE quiz_num = {3} ".format(table,1,1,1)
            cursor.execute(sql)
            sql = "UPDATE {0} SET clear_count = {1}, fail_count = {2} WHERE quiz_num = {3} ".format(table,1,2,2)
            cursor.execute(sql)
            sql = "UPDATE {0} SET clear_count = {1}, fail_count = {2} WHERE quiz_num = {3} ".format(table,1,3,3)
            cursor.execute(sql)
            sql = "UPDATE {0} SET clear_count = {1}, fail_count = {2} WHERE quiz_num = {3} ".format(table,1,4,4)
            cursor.execute(sql)
            sql = "UPDATE {0} SET clear_count = {1}, fail_count = {2} WHERE quiz_num = {3} ".format(table,1,5,5)
            cursor.execute(sql)
            # コミット
            conn.commit()

        # 最低正解率データ取得
        response = worst_quiz.worst_quiz(file_num=file_num)
        self.assertEqual(response['statusCode'],200)
        result = response['result']
        self.assertEqual(len(result),1)
        self.assertEqual(result[0]['quiz_num'],5)
        self.assertEqual(result[0]['quiz_sentense'],'worst_quizテスト5問題')
        self.assertEqual(result[0]['answer'],'worst_quizテスト5答え')
        self.assertEqual(result[0]['clear_count'],1)
        self.assertEqual(result[0]['fail_count'],5)
        self.assertEqual(result[0]['category'],'worst_quizテスト5カテゴリ')
        self.assertEqual(result[0]['img_file'],'worst_quizテスト5画像')
        self.assertEqual(result[0]['checked'],0)
        self.assertEqual(result[0]['deleted'],0)
        self.assertEqual(result[0]['accuracy_rate'],'16.7')

        with conn.cursor() as cursor:
            # 終わったらテストデータ削除
            sql = "DELETE FROM {0} ".format(table)
            cursor.execute(sql)

        # 全て成功したらコミット
        conn.commit()
        conn.close()

if __name__ == '__main__':
    unittest.main()

