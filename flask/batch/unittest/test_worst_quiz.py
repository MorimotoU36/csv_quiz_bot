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
from ini import get_messages_ini

from ut_common import delete_all_quiz_of_file

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
            # 正解率操作
            sql = "UPDATE quiz SET clear_count = {0}, fail_count = {1} WHERE file_num = {2} AND quiz_num = {3}".format(1,1,file_num,1)
            cursor.execute(sql)
            sql = "UPDATE quiz SET clear_count = {0}, fail_count = {1} WHERE file_num = {2} AND quiz_num = {3}".format(1,2,file_num,2)
            cursor.execute(sql)
            sql = "UPDATE quiz SET clear_count = {0}, fail_count = {1} WHERE file_num = {2} AND quiz_num = {3}".format(1,3,file_num,3)
            cursor.execute(sql)
            sql = "UPDATE quiz SET clear_count = {0}, fail_count = {1} WHERE file_num = {2} AND quiz_num = {3}".format(1,4,file_num,4)
            cursor.execute(sql)
            sql = "UPDATE quiz SET clear_count = {0}, fail_count = {1} WHERE file_num = {2} AND quiz_num = {3}".format(1,5,file_num,5)
            cursor.execute(sql)

            # コミット
            conn.commit()

        # 最低正解率データ取得
        response = worst_quiz.worst_quiz(file_num=file_num)
        self.assertEqual(response['statusCode'],200)
        result = response['result']
        self.assertEqual(len(result),1)
        self.assertEqual(result[0]['file_num'],0)
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

        # 終わったらテストデータ削除
        self.assertEqual(delete_all_quiz_of_file(conn,file_num),0)

        # 全て成功したらコミット
        conn.commit()
        conn.close()

if __name__ == '__main__':
    unittest.main()

