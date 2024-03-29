# -*- coding: utf-8 -*-
import os
import sys
import time
import traceback
import pymysql
import pymysql.cursors

import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
import minimum_quiz
import add_quiz

sys.path.append(os.path.join(os.path.dirname(__file__), '../module'))
from dbconfig import get_connection
from ini import get_messages_ini

from ut_common import delete_all_quiz_of_file

class TestMinimumQuiz(unittest.TestCase):

    # 問題を1つ取ってくるテスト
    def test_minimum_quiz(self):

        # 入力データ
        input_data = "\n".join(["minimum_quizテスト1問題,minimum_quizテスト1答え,minimum_quizテスト1カテゴリ,minimum_quizテスト1画像"
                                ,"minimum_quizテスト2問題,minimum_quizテスト2答え,minimum_quizテスト2カテゴリ,minimum_quizテスト2画像"
                                ,"minimum_quizテスト3問題,minimum_quizテスト3答え,minimum_quizテスト3カテゴリ,minimum_quizテスト3画像"
                                ,"minimum_quizテスト4問題,minimum_quizテスト4答え,minimum_quizテスト4カテゴリ,minimum_quizテスト4画像"
                                ,"minimum_quizテスト5問題,minimum_quizテスト5答え,minimum_quizテスト5カテゴリ,minimum_quizテスト5画像"])
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

        # テスト用テーブルのデータ全件削除
        self.assertEqual(delete_all_quiz_of_file(conn,file_num),0)

        # データ追加
        add_quiz.add_quiz(file_num,input_data)

        with conn.cursor() as cursor:
            # 正解数操作
            sql = "UPDATE quiz SET clear_count = {0}, fail_count = {1} WHERE file_num = {2} AND quiz_num = {3}".format(5,1,file_num,1)
            cursor.execute(sql)
            sql = "UPDATE quiz SET clear_count = {0}, fail_count = {1} WHERE file_num = {2} AND quiz_num = {3}".format(4,2,file_num,2)
            cursor.execute(sql)
            sql = "UPDATE quiz SET clear_count = {0}, fail_count = {1} WHERE file_num = {2} AND quiz_num = {3}".format(3,3,file_num,3)
            cursor.execute(sql)
            sql = "UPDATE quiz SET clear_count = {0}, fail_count = {1} WHERE file_num = {2} AND quiz_num = {3}".format(2,4,file_num,4)
            cursor.execute(sql)
            sql = "UPDATE quiz SET clear_count = {0}, fail_count = {1} WHERE file_num = {2} AND quiz_num = {3}".format(1,5,file_num,5)
            cursor.execute(sql)
            # コミット
            conn.commit()

        # 最低正解率データ取得
        response = minimum_quiz.minimum_quiz(file_num=file_num)
        self.assertEqual(response['statusCode'],200)
        result = response['result']
        self.assertEqual(len(result),1)
        self.assertEqual(result[0]['file_num'],0)
        self.assertEqual(result[0]['quiz_num'],5)
        self.assertEqual(result[0]['quiz_sentense'],'minimum_quizテスト5問題')
        self.assertEqual(result[0]['answer'],'minimum_quizテスト5答え')
        self.assertEqual(result[0]['clear_count'],1)
        self.assertEqual(result[0]['fail_count'],5)
        self.assertEqual(result[0]['category'],'minimum_quizテスト5カテゴリ')
        self.assertEqual(result[0]['img_file'],'minimum_quizテスト5画像')
        self.assertEqual(result[0]['checked'],0)
        self.assertEqual(result[0]['deleted'],0)
        self.assertEqual(result[0]['accuracy_rate'],'16.7')

        # 終わったらテストデータ削除
        self.assertEqual(delete_all_quiz_of_file(conn,file_num),0)

        # 全て成功したらコミット
        conn.commit()
        conn.close()

if __name__ == '__main__':
    unittest.main()

