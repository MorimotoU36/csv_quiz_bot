# -*- coding: utf-8 -*-
import os
import sys
import time
import traceback
import pymysql
import pymysql.cursors

# unittestインポート
import unittest

# テスト対象ファイルインポート
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
import add_quiz
import delete_quiz

sys.path.append(os.path.join(os.path.dirname(__file__), '../module'))
from dbconfig import get_connection
from ini import get_table_list

# テストクラス作成(Testから始まる名前にする、unittest.TestCaseを継承する)
class TestAddQuiz(unittest.TestCase):

    # 問題を1つ追加するテスト
    def test_add_a_quiz(self):

        # 入力データ
        input_data = "add_quizテスト1問題,add_quizテスト1答え,add_quizテスト1カテゴリ,add_quizテスト1画像"
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
            # 件数確認(1件追加されたか)
            sql = "SELECT count(*) FROM {0} ".format(table)
            cursor.execute(sql)
            sql_results = cursor.fetchall()
            self.assertEqual(sql_results[0]['count(*)'],1)

            # 追加されたデータを確認
            sql = "SELECT * FROM {0} LIMIT 1".format(table)
            cursor.execute(sql)
            sql_results = cursor.fetchall()
            self.assertEqual(sql_results[0]['quiz_num'],1)
            self.assertEqual(sql_results[0]['quiz_sentense'],'add_quizテスト1問題')
            self.assertEqual(sql_results[0]['answer'],'add_quizテスト1答え')
            self.assertEqual(sql_results[0]['clear_count'],0)
            self.assertEqual(sql_results[0]['fail_count'],0)
            self.assertEqual(sql_results[0]['category'],'add_quizテスト1カテゴリ')
            self.assertEqual(sql_results[0]['img_file'],'add_quizテスト1画像')
            self.assertEqual(sql_results[0]['checked'],0)
            self.assertEqual(sql_results[0]['deleted'],0)

            # 終わったらテストデータ削除
            sql = "DELETE FROM {0} ".format(table)
            cursor.execute(sql)

        # 全て成功したらコミット
        conn.commit()
        conn.close()

    # 問題を複数(ここでは3つ)追加するテスト
    def test_add_quizs(self):

        # 入力データ（改行区切り）
        input_data = '\n'.join(["add_quizテスト1-1問題,add_quizテスト1-1答え,add_quizテスト1-1カテゴリ,add_quizテスト1-1画像",
                    "add_quizテスト1-2問題,add_quizテスト1-2答え,add_quizテスト1-2カテゴリ,add_quizテスト1-2画像",
                    "add_quizテスト1-3問題,add_quizテスト1-3答え,add_quizテスト1-3カテゴリ,add_quizテスト1-3画像"])
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
            # 件数確認(3件追加されたか)
            sql = "SELECT count(*) FROM {0} ".format(table)
            cursor.execute(sql)
            sql_results = cursor.fetchall()
            self.assertEqual(sql_results[0]['count(*)'],3)

            # 追加されたデータを確認
            sql = "SELECT * FROM {0} ORDER BY quiz_sentense".format(table)
            cursor.execute(sql)
            sql_results = cursor.fetchall()
            self.assertEqual(sql_results[0]['quiz_num'],1)
            self.assertEqual(sql_results[0]['quiz_sentense'],'add_quizテスト1-1問題')
            self.assertEqual(sql_results[0]['answer'],'add_quizテスト1-1答え')
            self.assertEqual(sql_results[0]['clear_count'],0)
            self.assertEqual(sql_results[0]['fail_count'],0)
            self.assertEqual(sql_results[0]['category'],'add_quizテスト1-1カテゴリ')
            self.assertEqual(sql_results[0]['img_file'],'add_quizテスト1-1画像')
            self.assertEqual(sql_results[0]['checked'],0)
            self.assertEqual(sql_results[0]['deleted'],0)

            self.assertEqual(sql_results[1]['quiz_num'],2)
            self.assertEqual(sql_results[1]['quiz_sentense'],'add_quizテスト1-2問題')
            self.assertEqual(sql_results[1]['answer'],'add_quizテスト1-2答え')
            self.assertEqual(sql_results[1]['clear_count'],0)
            self.assertEqual(sql_results[1]['fail_count'],0)
            self.assertEqual(sql_results[1]['category'],'add_quizテスト1-2カテゴリ')
            self.assertEqual(sql_results[1]['img_file'],'add_quizテスト1-2画像')
            self.assertEqual(sql_results[1]['checked'],0)
            self.assertEqual(sql_results[1]['deleted'],0)

            self.assertEqual(sql_results[2]['quiz_num'],3)
            self.assertEqual(sql_results[2]['quiz_sentense'],'add_quizテスト1-3問題')
            self.assertEqual(sql_results[2]['answer'],'add_quizテスト1-3答え')
            self.assertEqual(sql_results[2]['clear_count'],0)
            self.assertEqual(sql_results[2]['fail_count'],0)
            self.assertEqual(sql_results[2]['category'],'add_quizテスト1-3カテゴリ')
            self.assertEqual(sql_results[2]['img_file'],'add_quizテスト1-3画像')
            self.assertEqual(sql_results[2]['checked'],0)
            self.assertEqual(sql_results[2]['deleted'],0)

            # 終わったらテストデータ削除
            sql = "DELETE FROM {0} ".format(table)
            cursor.execute(sql)

        # 全て成功したらコミット
        conn.commit()
        conn.close()


    # 削除済問題のところに問題を追加するテスト
    def test_add_quiz_to_deleted(self):

        # 入力データ（改行区切り）
        input_data = '\n'.join(["add_quizテスト2-1問題,add_quizテスト2-1答え,add_quizテスト2-1カテゴリ,add_quizテスト2-1画像",
                    "add_quizテスト2-2問題,add_quizテスト2-2答え,add_quizテスト2-2カテゴリ,add_quizテスト2-2画像",
                    "add_quizテスト2-3問題,add_quizテスト2-3答え,add_quizテスト2-3カテゴリ,add_quizテスト2-3画像"])
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
            # コミット
            conn.commit()

        # データ追加
        resp = add_quiz.add_quiz(file_num,input_data)
        # 追加したデータを削除
        resp = delete_quiz.delete_quiz(file_num,1)
        resp = delete_quiz.delete_quiz(file_num,2)

        with conn.cursor() as cursor:
            # 件数確認(3件追加されたか)
            sql = "SELECT count(*) FROM {0} ".format(table)
            cursor.execute(sql)
            sql_results = cursor.fetchall()
            self.assertEqual(sql_results[0]['count(*)'],3)

            # 件数確認(削除されたデータ)
            sql = "SELECT count(*) FROM {0} WHERE deleted = 1 ".format(table)
            cursor.execute(sql)
            sql_results = cursor.fetchall()
            self.assertEqual(sql_results[0]['count(*)'],2)

            # コミット
            conn.commit()

        # データ再度追加（削除済の箇所に入る）
        resp = add_quiz.add_quiz(file_num,"add_quizテスト2-4問題,add_quizテスト2-4答え,add_quizテスト2-4カテゴリ,add_quizテスト2-4画像")

        with conn.cursor() as cursor:
            # 追加されたデータを確認
            sql = "SELECT * FROM {0} ORDER BY quiz_num".format(table)
            cursor.execute(sql)
            sql_results = cursor.fetchall()
            self.assertEqual(sql_results[0]['quiz_num'],1)
            self.assertEqual(sql_results[0]['quiz_sentense'],'add_quizテスト2-4問題')
            self.assertEqual(sql_results[0]['answer'],'add_quizテスト2-4答え')
            self.assertEqual(sql_results[0]['clear_count'],0)
            self.assertEqual(sql_results[0]['fail_count'],0)
            self.assertEqual(sql_results[0]['category'],'add_quizテスト2-4カテゴリ')
            self.assertEqual(sql_results[0]['img_file'],'add_quizテスト2-4画像')
            self.assertEqual(sql_results[0]['checked'],0)
            self.assertEqual(sql_results[0]['deleted'],0)

            self.assertEqual(sql_results[1]['quiz_num'],2)
            self.assertEqual(sql_results[1]['quiz_sentense'],'add_quizテスト2-2問題')
            self.assertEqual(sql_results[1]['answer'],'add_quizテスト2-2答え')
            self.assertEqual(sql_results[1]['clear_count'],0)
            self.assertEqual(sql_results[1]['fail_count'],0)
            self.assertEqual(sql_results[1]['category'],'add_quizテスト2-2カテゴリ')
            self.assertEqual(sql_results[1]['img_file'],'add_quizテスト2-2画像')
            self.assertEqual(sql_results[1]['checked'],0)
            self.assertEqual(sql_results[1]['deleted'],1)

            self.assertEqual(sql_results[2]['quiz_num'],3)
            self.assertEqual(sql_results[2]['quiz_sentense'],'add_quizテスト2-3問題')
            self.assertEqual(sql_results[2]['answer'],'add_quizテスト2-3答え')
            self.assertEqual(sql_results[2]['clear_count'],0)
            self.assertEqual(sql_results[2]['fail_count'],0)
            self.assertEqual(sql_results[2]['category'],'add_quizテスト2-3カテゴリ')
            self.assertEqual(sql_results[2]['img_file'],'add_quizテスト2-3画像')
            self.assertEqual(sql_results[2]['checked'],0)
            self.assertEqual(sql_results[2]['deleted'],0)

            # 終わったらテストデータ削除
            sql = "DELETE FROM {0} ".format(table)
            cursor.execute(sql)

        # 全て成功したらコミット
        conn.commit()
        conn.close()


# 全テスト実行
if __name__ == '__main__':
    unittest.main()