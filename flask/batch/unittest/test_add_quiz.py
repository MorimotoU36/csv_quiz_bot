# -*- coding: utf-8 -*-
import os
import sys
import traceback
import pymysql
import pymysql.cursors

# unittestインポート
import unittest

# テスト対象ファイルインポート
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
import add_quiz

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
        file_num = 2

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



# 全テスト実行
if __name__ == '__main__':
    unittest.main()