# -*- coding: utf-8 -*-
import os
import sys
import time
import traceback
import pymysql
import pymysql.cursors

import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
import integrate_quiz
import add_quiz

sys.path.append(os.path.join(os.path.dirname(__file__), '../module'))
from dbconfig import get_connection
from ini import get_table_list, get_messages_ini

class TestIntegrateQuiz(unittest.TestCase):

    # 問題を1つ統合するテスト
    def test_integrate_quiz(self):

        # 入力データ
        input_data = "\n".join(["integrate_quizテスト1問題,integrate_quizテスト1答え,integrate_quizテスト1カテゴリ,integrate_quizテスト1画像"
                                ,"integrate_quizテスト2問題,integrate_quizテスト2答え,integrate_quizテスト2カテゴリ,integrate_quizテスト2画像"
                                ,"integrate_quizテスト3問題,integrate_quizテスト3答え,integrate_quizテスト3カテゴリ,integrate_quizテスト3画像"
                                ,"integrate_quizテスト4問題,integrate_quizテスト4答え,integrate_quizテスト4カテゴリ,integrate_quizテスト4画像"
                                ,"integrate_quizテスト5問題,integrate_quizテスト5答え,integrate_quizテスト5カテゴリ,integrate_quizテスト5画像"])
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

        with conn.cursor() as cursor:
            # 正解数操作
            sql = "UPDATE {0} SET clear_count = {1}, fail_count = {2} WHERE quiz_num = {3} ".format(table,20,10,1)
            cursor.execute(sql)
            sql = "UPDATE {0} SET clear_count = {1}, fail_count = {2} WHERE quiz_num = {3} ".format(table,1,2,2)
            cursor.execute(sql)
            # コミット
            conn.commit()

        # データ統合(No.1->No.2)
        integrate_quiz.integrate_quiz(0,1,0,2)

        # データ取得
        with conn.cursor() as cursor:
            sql = "SELECT * FROM {0} ORDER BY quiz_num".format(table)
            cursor.execute(sql)
            result = cursor.fetchall()
            self.assertEqual(len(result),5)
            self.assertEqual(result[0]['quiz_num'],1)
            self.assertEqual(result[0]['quiz_sentense'],'integrate_quizテスト1問題')
            self.assertEqual(result[0]['answer'],'integrate_quizテスト1答え')
            self.assertEqual(result[0]['clear_count'],20)
            self.assertEqual(result[0]['fail_count'],10)
            self.assertEqual(result[0]['category'],'integrate_quizテスト1カテゴリ')
            self.assertEqual(result[0]['img_file'],'integrate_quizテスト1画像')
            self.assertEqual(result[0]['checked'],0)
            self.assertEqual(result[0]['deleted'],1)

            self.assertEqual(result[1]['quiz_num'],2)
            self.assertEqual(result[1]['quiz_sentense'],'integrate_quizテスト2問題')
            self.assertEqual(result[1]['answer'],'integrate_quizテスト2答え')
            self.assertEqual(result[1]['clear_count'],21)
            self.assertEqual(result[1]['fail_count'],12)
            self.assertEqual(result[1]['category'],'integrate_quizテスト1カテゴリ:integrate_quizテスト2カテゴリ')
            self.assertEqual(result[1]['img_file'],'integrate_quizテスト2画像')
            self.assertEqual(result[1]['checked'],0)
            self.assertEqual(result[1]['deleted'],0)

        with conn.cursor() as cursor:
            # 終わったらテストデータ削除
            sql = "DELETE FROM {0} ".format(table)
            cursor.execute(sql)

        # 全て成功したらコミット
        conn.commit()
        conn.close()


if __name__ == '__main__':
    unittest.main()