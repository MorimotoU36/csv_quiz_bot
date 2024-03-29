# -*- coding: utf-8 -*-
import os
import sys
import time
import traceback
import pymysql
import pymysql.cursors

import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
import edit_quiz
import select_quiz
import add_quiz

sys.path.append(os.path.join(os.path.dirname(__file__), '../module'))
from dbconfig import get_connection, get_file_info
from ini import get_messages_ini

from ut_common import delete_all_quiz_of_file

class TestEditQuiz(unittest.TestCase):

    # 問題を1つ編集するテスト
    def test_edit_quiz(self):

        # 入力データ
        input_data = "\n".join(["edit_quizテスト1問題,edit_quizテスト1答え,edit_quizテスト1カテゴリ,edit_quizテスト1画像"
                                ,"edit_quizテスト2問題,edit_quizテスト2答え,edit_quizテスト2カテゴリ,edit_quizテスト2画像"
                                ,"edit_quizテスト3問題,edit_quizテスト3答え,edit_quizテスト3カテゴリ,edit_quizテスト3画像"
                                ,"edit_quizテスト4問題,edit_quizテスト4答え,edit_quizテスト4カテゴリ,edit_quizテスト4画像"
                                ,"edit_quizテスト5問題,edit_quizテスト5答え,edit_quizテスト5カテゴリ,edit_quizテスト5画像"])
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

        # データ編集
        edit_quiz.edit_quiz(0,1,"編集後問題1","編集後答え1","編集後カテゴリ1","編集後画像1")

        # データ取得
        response = select_quiz.select_quiz(file_num,1)

        self.assertEqual(response['statusCode'],200)
        result = response['result']
        self.assertEqual(len(result),1)
        self.assertEqual(result[0]['file_num'],0)
        self.assertEqual(result[0]['quiz_num'],1)
        self.assertEqual(result[0]['quiz_sentense'],'編集後問題1')
        self.assertEqual(result[0]['answer'],'編集後答え1')
        self.assertEqual(result[0]['clear_count'],0)
        self.assertEqual(result[0]['fail_count'],0)
        self.assertEqual(result[0]['category'],'編集後カテゴリ1')
        self.assertEqual(result[0]['img_file'],'編集後画像1')
        self.assertEqual(result[0]['checked'],0)
        self.assertEqual(result[0]['deleted'],0)
        self.assertEqual(result[0]['accuracy_rate'],'0')

        # 終わったらテストデータ削除
        self.assertEqual(delete_all_quiz_of_file(conn,file_num),0)

        # 全て成功したらコミット
        conn.commit()
        conn.close()

    # 問題のカテゴリを1つ編集するテスト
    def test_edit_category_of_question(self):

        # 入力データ
        input_data = "\n".join(["edit_quizテスト1問題,edit_quizテスト1答え,edit_quizテスト1カテゴリ,edit_quizテスト1画像"
                                ,"edit_quizテスト2問題,edit_quizテスト2答え,edit_quizテスト2カテゴリ,edit_quizテスト2画像"
                                ,"edit_quizテスト3問題,edit_quizテスト3答え,edit_quizテスト3カテゴリ,edit_quizテスト3画像"
                                ,"edit_quizテスト4問題,edit_quizテスト4答え,edit_quizテスト4カテゴリ,edit_quizテスト4画像"
                                ,"edit_quizテスト5問題,edit_quizテスト5答え,edit_quizテスト5カテゴリ,edit_quizテスト5画像"])
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

        # カテゴリ追加
        response = edit_quiz.edit_category_of_question([{
            "file_num": file_num,
            "quiz_num": 1,
            "category": "カテゴリ追加テスト"
        }])

        # データ取得
        response = select_quiz.select_quiz(file_num,1)

        self.assertEqual(response['statusCode'],200)
        result = response['result']
        self.assertEqual(len(result),1)
        self.assertEqual(result[0]['file_num'],0)
        self.assertEqual(result[0]['quiz_num'],1)
        self.assertEqual(result[0]['quiz_sentense'],'edit_quizテスト1問題')
        self.assertEqual(result[0]['answer'],'edit_quizテスト1答え')
        self.assertEqual(result[0]['clear_count'],0)
        self.assertEqual(result[0]['fail_count'],0)
        self.assertEqual(result[0]['category'],'edit_quizテスト1カテゴリ:カテゴリ追加テスト')
        self.assertEqual(result[0]['img_file'],'edit_quizテスト1画像')
        self.assertEqual(result[0]['checked'],0)
        self.assertEqual(result[0]['deleted'],0)
        self.assertEqual(result[0]['accuracy_rate'],'0')

        # 終わったらテストデータ削除
        self.assertEqual(delete_all_quiz_of_file(conn,file_num),0)

        # 全て成功したらコミット
        conn.commit()
        conn.close()


    # 問題のチェックを1つ編集するテスト
    def test_edit_checked_of_question(self):

        # 入力データ
        input_data = "\n".join(["edit_quizテスト1問題,edit_quizテスト1答え,edit_quizテスト1カテゴリ,edit_quizテスト1画像"
                                ,"edit_quizテスト2問題,edit_quizテスト2答え,edit_quizテスト2カテゴリ,edit_quizテスト2画像"
                                ,"edit_quizテスト3問題,edit_quizテスト3答え,edit_quizテスト3カテゴリ,edit_quizテスト3画像"
                                ,"edit_quizテスト4問題,edit_quizテスト4答え,edit_quizテスト4カテゴリ,edit_quizテスト4画像"
                                ,"edit_quizテスト5問題,edit_quizテスト5答え,edit_quizテスト5カテゴリ,edit_quizテスト5画像"])
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

        # チェック追加
        response = edit_quiz.edit_checked_of_question([{
            "file_num": file_num,
            "quiz_num": 1
        }])

        # データ取得
        response = select_quiz.select_quiz(file_num,1)

        self.assertEqual(response['statusCode'],200)
        result = response['result']
        self.assertEqual(len(result),1)
        self.assertEqual(result[0]['file_num'],0)
        self.assertEqual(result[0]['quiz_num'],1)
        self.assertEqual(result[0]['quiz_sentense'],'edit_quizテスト1問題')
        self.assertEqual(result[0]['answer'],'edit_quizテスト1答え')
        self.assertEqual(result[0]['clear_count'],0)
        self.assertEqual(result[0]['fail_count'],0)
        self.assertEqual(result[0]['category'],'edit_quizテスト1カテゴリ')
        self.assertEqual(result[0]['img_file'],'edit_quizテスト1画像')
        self.assertEqual(result[0]['checked'],1)
        self.assertEqual(result[0]['deleted'],0)
        self.assertEqual(result[0]['accuracy_rate'],'0')

        # チェック削除
        response = edit_quiz.edit_checked_of_question([{
            "file_num": file_num,
            "quiz_num": 1
        }])

        # データ取得
        response = select_quiz.select_quiz(file_num,1)

        self.assertEqual(response['statusCode'],200)
        result = response['result']
        self.assertEqual(len(result),1)
        self.assertEqual(result[0]['file_num'],0)
        self.assertEqual(result[0]['quiz_num'],1)
        self.assertEqual(result[0]['quiz_sentense'],'edit_quizテスト1問題')
        self.assertEqual(result[0]['answer'],'edit_quizテスト1答え')
        self.assertEqual(result[0]['clear_count'],0)
        self.assertEqual(result[0]['fail_count'],0)
        self.assertEqual(result[0]['category'],'edit_quizテスト1カテゴリ')
        self.assertEqual(result[0]['img_file'],'edit_quizテスト1画像')
        self.assertEqual(result[0]['checked'],0)
        self.assertEqual(result[0]['deleted'],0)
        self.assertEqual(result[0]['accuracy_rate'],'0')

        # 終わったらテストデータ削除
        self.assertEqual(delete_all_quiz_of_file(conn,file_num),0)

        # 全て成功したらコミット
        conn.commit()
        conn.close()

if __name__ == '__main__':
    unittest.main()