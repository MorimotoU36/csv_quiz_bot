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
from ini import get_messages_ini

from ut_common import delete_all_quiz_of_file

class TestRandomQuiz(unittest.TestCase):

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

        # データ取得
        response = random_quiz.random_quiz(file_num=file_num)
        self.assertEqual(response['statusCode'],200)
        result = response['result']
        self.assertEqual(len(result),1)
        self.assertEqual(result[0]['file_num'],0)
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

        # 終わったらテストデータ削除
        self.assertEqual(delete_all_quiz_of_file(conn,file_num),0)

        # 全て成功したらコミット
        conn.commit()
        conn.close()

    # 正解率指定に関係なく正解率NULLの問題を取れるかのテスト
    def test_get_null_rate_quiz(self):

        # 入力データ
        input_data = "\n".join(["random_quizテスト1問題,random_quizテスト1答え,random_quizテスト1カテゴリ,random_quizテスト1画像"
                                ,"random_quizテスト2問題,random_quizテスト2答え,random_quizテスト2カテゴリ,random_quizテスト2画像"
                                ,"random_quizテスト3問題,random_quizテスト3答え,random_quizテスト3カテゴリ,random_quizテスト3画像"
                                ,"random_quizテスト4問題,random_quizテスト4答え,random_quizテスト4カテゴリ,random_quizテスト4画像"
                                ,"random_quizテスト5問題,random_quizテスト5答え,random_quizテスト5カテゴリ,random_quizテスト5画像"])
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

        # データ取得
        response = random_quiz.random_quiz(file_num=file_num,min_rate=50,max_rate=50)
        self.assertEqual(response['statusCode'],200)
        result = response['result']
        self.assertEqual(len(result),1)
        self.assertEqual(result[0]['file_num'],0)
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

        # 終わったらテストデータ削除
        self.assertEqual(delete_all_quiz_of_file(conn,file_num),0)

        # 全て成功したらコミット
        conn.commit()
        conn.close()

    # 最小正解率指定時に該当する問題のみを取れるかのテスト
    def test_min_rate(self):

        # 入力データ
        input_data = "\n".join(["random_quizテスト1問題,random_quizテスト1答え,random_quizテスト1カテゴリ,random_quizテスト1画像"
                                ,"random_quizテスト2問題,random_quizテスト2答え,random_quizテスト2カテゴリ,random_quizテスト2画像"
                                ,"random_quizテスト3問題,random_quizテスト3答え,random_quizテスト3カテゴリ,random_quizテスト3画像"
                                ,"random_quizテスト4問題,random_quizテスト4答え,random_quizテスト4カテゴリ,random_quizテスト4画像"
                                ,"random_quizテスト5問題,random_quizテスト5答え,random_quizテスト5カテゴリ,random_quizテスト5画像"])
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
            # 20%
            sql = "UPDATE quiz SET clear_count = {0}, fail_count = {1} WHERE file_num = {2} AND quiz_num = {3}".format(2,8,file_num,1)
            cursor.execute(sql)
            # 40%
            sql = "UPDATE quiz SET clear_count = {0}, fail_count = {1} WHERE file_num = {2} AND quiz_num = {3}".format(4,6,file_num,2)
            cursor.execute(sql)
            # 60%
            sql = "UPDATE quiz SET clear_count = {0}, fail_count = {1} WHERE file_num = {2} AND quiz_num = {3}".format(6,4,file_num,3)
            cursor.execute(sql)
            # 80%
            sql = "UPDATE quiz SET clear_count = {0}, fail_count = {1} WHERE file_num = {2} AND quiz_num = {3}".format(8,2,file_num,4)
            cursor.execute(sql)
            # 100%
            sql = "UPDATE quiz SET clear_count = {0}, fail_count = {1} WHERE file_num = {2} AND quiz_num = {3}".format(10,0,file_num,5)
            cursor.execute(sql)
            # コミット
            conn.commit()

        # データ取得
        response = random_quiz.random_quiz(file_num=file_num,min_rate=90)
        self.assertEqual(response['statusCode'],200)
        result = response['result']
        self.assertEqual(len(result),1)
        self.assertEqual(result[0]['file_num'],0)
        self.assertEqual(result[0]['quiz_num'],5)
        self.assertEqual(result[0]['quiz_sentense'],'random_quizテスト5問題')
        self.assertEqual(result[0]['answer'],'random_quizテスト5答え')
        self.assertEqual(result[0]['clear_count'],10)
        self.assertEqual(result[0]['fail_count'],0)
        self.assertEqual(result[0]['category'],'random_quizテスト5カテゴリ')
        self.assertEqual(result[0]['img_file'],'random_quizテスト5画像')
        self.assertEqual(result[0]['checked'],0)
        self.assertEqual(result[0]['deleted'],0)
        self.assertEqual(result[0]['accuracy_rate'],'100.0')

        # 終わったらテストデータ削除
        self.assertEqual(delete_all_quiz_of_file(conn,file_num),0)

        # 全て成功したらコミット
        conn.commit()
        conn.close()


    # 最大正解率指定時に該当する問題のみを取れるかのテスト
    def test_max_rate(self):

        # 入力データ
        input_data = "\n".join(["random_quizテスト1問題,random_quizテスト1答え,random_quizテスト1カテゴリ,random_quizテスト1画像"
                                ,"random_quizテスト2問題,random_quizテスト2答え,random_quizテスト2カテゴリ,random_quizテスト2画像"
                                ,"random_quizテスト3問題,random_quizテスト3答え,random_quizテスト3カテゴリ,random_quizテスト3画像"
                                ,"random_quizテスト4問題,random_quizテスト4答え,random_quizテスト4カテゴリ,random_quizテスト4画像"
                                ,"random_quizテスト5問題,random_quizテスト5答え,random_quizテスト5カテゴリ,random_quizテスト5画像"])
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
            # 20%
            sql = "UPDATE quiz SET clear_count = {0}, fail_count = {1} WHERE file_num = {2} AND quiz_num = {3}".format(2,8,file_num,1)
            cursor.execute(sql)
            # 40%
            sql = "UPDATE quiz SET clear_count = {0}, fail_count = {1} WHERE file_num = {2} AND quiz_num = {3}".format(4,6,file_num,2)
            cursor.execute(sql)
            # 60%
            sql = "UPDATE quiz SET clear_count = {0}, fail_count = {1} WHERE file_num = {2} AND quiz_num = {3}".format(6,4,file_num,3)
            cursor.execute(sql)
            # 80%
            sql = "UPDATE quiz SET clear_count = {0}, fail_count = {1} WHERE file_num = {2} AND quiz_num = {3}".format(8,2,file_num,4)
            cursor.execute(sql)
            # 100%
            sql = "UPDATE quiz SET clear_count = {0}, fail_count = {1} WHERE file_num = {2} AND quiz_num = {3}".format(10,0,file_num,5)
            cursor.execute(sql)
            # コミット
            conn.commit()

        # データ取得
        response = random_quiz.random_quiz(file_num=file_num,max_rate=25)
        self.assertEqual(response['statusCode'],200)
        result = response['result']
        self.assertEqual(len(result),1)
        self.assertEqual(result[0]['file_num'],0)
        self.assertEqual(result[0]['quiz_num'],1)
        self.assertEqual(result[0]['quiz_sentense'],'random_quizテスト1問題')
        self.assertEqual(result[0]['answer'],'random_quizテスト1答え')
        self.assertEqual(result[0]['clear_count'],2)
        self.assertEqual(result[0]['fail_count'],8)
        self.assertEqual(result[0]['category'],'random_quizテスト1カテゴリ')
        self.assertEqual(result[0]['img_file'],'random_quizテスト1画像')
        self.assertEqual(result[0]['checked'],0)
        self.assertEqual(result[0]['deleted'],0)
        self.assertEqual(result[0]['accuracy_rate'],'20.0')

        # 終わったらテストデータ削除
        self.assertEqual(delete_all_quiz_of_file(conn,file_num),0)

        # 全て成功したらコミット
        conn.commit()
        conn.close()

    # 最小最大正解率指定時に該当する問題のみを取れるかのテスト
    def test_min_max_rate(self):

        # 入力データ
        input_data = "\n".join(["random_quizテスト1問題,random_quizテスト1答え,random_quizテスト1カテゴリ,random_quizテスト1画像"
                                ,"random_quizテスト2問題,random_quizテスト2答え,random_quizテスト2カテゴリ,random_quizテスト2画像"
                                ,"random_quizテスト3問題,random_quizテスト3答え,random_quizテスト3カテゴリ,random_quizテスト3画像"
                                ,"random_quizテスト4問題,random_quizテスト4答え,random_quizテスト4カテゴリ,random_quizテスト4画像"
                                ,"random_quizテスト5問題,random_quizテスト5答え,random_quizテスト5カテゴリ,random_quizテスト5画像"])
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
            # 20%
            sql = "UPDATE quiz SET clear_count = {0}, fail_count = {1} WHERE file_num = {2} AND quiz_num = {3}".format(2,8,file_num,1)
            cursor.execute(sql)
            # 40%
            sql = "UPDATE quiz SET clear_count = {0}, fail_count = {1} WHERE file_num = {2} AND quiz_num = {3}".format(4,6,file_num,2)
            cursor.execute(sql)
            # 60%
            sql = "UPDATE quiz SET clear_count = {0}, fail_count = {1} WHERE file_num = {2} AND quiz_num = {3}".format(6,4,file_num,3)
            cursor.execute(sql)
            # 80%
            sql = "UPDATE quiz SET clear_count = {0}, fail_count = {1} WHERE file_num = {2} AND quiz_num = {3}".format(8,2,file_num,4)
            cursor.execute(sql)
            # 100%
            sql = "UPDATE quiz SET clear_count = {0}, fail_count = {1} WHERE file_num = {2} AND quiz_num = {3}".format(10,0,file_num,5)
            cursor.execute(sql)
            # コミット
            conn.commit()

        # データ取得
        response = random_quiz.random_quiz(file_num=file_num,min_rate=60,max_rate=60)
        self.assertEqual(response['statusCode'],200)
        result = response['result']
        self.assertEqual(len(result),1)
        self.assertEqual(result[0]['file_num'],0)
        self.assertEqual(result[0]['quiz_num'],3)
        self.assertEqual(result[0]['quiz_sentense'],'random_quizテスト3問題')
        self.assertEqual(result[0]['answer'],'random_quizテスト3答え')
        self.assertEqual(result[0]['clear_count'],6)
        self.assertEqual(result[0]['fail_count'],4)
        self.assertEqual(result[0]['category'],'random_quizテスト3カテゴリ')
        self.assertEqual(result[0]['img_file'],'random_quizテスト3画像')
        self.assertEqual(result[0]['checked'],0)
        self.assertEqual(result[0]['deleted'],0)
        self.assertEqual(result[0]['accuracy_rate'],'60.0')

        # 終わったらテストデータ削除
        self.assertEqual(delete_all_quiz_of_file(conn,file_num),0)

        # 全て成功したらコミット
        conn.commit()
        conn.close()

if __name__ == '__main__':
    unittest.main()