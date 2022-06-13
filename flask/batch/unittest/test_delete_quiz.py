# -*- coding: utf-8 -*-
import os
import sys
import time
import traceback
import pymysql
import pymysql.cursors

import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
import delete_quiz
import add_quiz

sys.path.append(os.path.join(os.path.dirname(__file__), '../module'))
from dbconfig import get_connection, get_file_info
from ini import get_messages_ini

from ut_common import delete_all_quiz_of_file
class TestDeleteQuiz(unittest.TestCase):

    # 問題を1つ削除するテスト
    def test_delete_quiz(self):

        # 入力データ
        input_data = "\n".join(["delete_quizテスト1問題,delete_quizテスト1答え,delete_quizテスト1カテゴリ,delete_quizテスト1画像"
                                ,"delete_quizテスト2問題,delete_quizテスト2答え,delete_quizテスト2カテゴリ,delete_quizテスト2画像"
                                ,"delete_quizテスト3問題,delete_quizテスト3答え,delete_quizテスト3カテゴリ,delete_quizテスト3画像"
                                ,"delete_quizテスト4問題,delete_quizテスト4答え,delete_quizテスト4カテゴリ,delete_quizテスト4画像"
                                ,"delete_quizテスト5問題,delete_quizテスト5答え,delete_quizテスト5カテゴリ,delete_quizテスト5画像"])
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
        messages = get_messages_ini()
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

        # データ削除
        delete_quiz.delete_quiz(0,1)

        # データ取得
        with conn.cursor() as cursor:
            sql = "SELECT * FROM quiz WHERE file_num = {0} ORDER BY quiz_num".format(file_num)
            cursor.execute(sql)
            result = cursor.fetchall()
            self.assertEqual(len(result),5)
            self.assertEqual(result[0]['file_num'],0)
            self.assertEqual(result[0]['quiz_num'],1)
            self.assertEqual(result[0]['quiz_sentense'],'delete_quizテスト1問題')
            self.assertEqual(result[0]['answer'],'delete_quizテスト1答え')
            self.assertEqual(result[0]['clear_count'],0)
            self.assertEqual(result[0]['fail_count'],0)
            self.assertEqual(result[0]['category'],'delete_quizテスト1カテゴリ')
            self.assertEqual(result[0]['img_file'],'delete_quizテスト1画像')
            self.assertEqual(result[0]['checked'],0)
            self.assertEqual(result[0]['deleted'],1)

            self.assertEqual(result[1]['quiz_num'],2)
            self.assertEqual(result[1]['deleted'],0)
            self.assertEqual(result[2]['quiz_num'],3)
            self.assertEqual(result[2]['deleted'],0)
            self.assertEqual(result[3]['quiz_num'],4)
            self.assertEqual(result[3]['deleted'],0)
            self.assertEqual(result[4]['quiz_num'],5)
            self.assertEqual(result[4]['deleted'],0)

            # 終わったらテストデータ削除
            self.assertEqual(delete_all_quiz_of_file(conn,file_num),0)

        # 全て成功したらコミット
        conn.commit()
        conn.close()


if __name__ == '__main__':
    unittest.main()