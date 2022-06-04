# -*- coding: utf-8 -*-
import os
import sys
import time
import traceback
import pymysql
import pymysql.cursors

import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
import update_category_master
import add_quiz

sys.path.append(os.path.join(os.path.dirname(__file__), '../module'))
from dbconfig import get_connection
from ini import get_table_list

class TestUpdateCategoryMaster(unittest.TestCase):

    # カテゴリマスタを登録するテスト
    def test_update_category_master(self):

        # 入力データ
        input_data = "\n".join(["update_category_masterテスト1問題,update_category_masterテスト1答え,update_category_masterテスト1カテゴリ,update_category_masterテスト1画像"
                                ,"update_category_masterテスト2問題,update_category_masterテスト2答え,update_category_masterテスト2カテゴリ,update_category_masterテスト2画像"
                                ,"update_category_masterテスト3問題,update_category_masterテスト3答え,update_category_masterテスト3カテゴリ,update_category_masterテスト3画像"
                                ,"update_category_masterテスト4問題,update_category_masterテスト4答え,update_category_masterテスト4カテゴリ,update_category_masterテスト4画像"
                                ,"update_category_masterテスト5問題,update_category_masterテスト5答え,update_category_masterテスト5カテゴリ,update_category_masterテスト5画像"])
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

        # データ編集
        update_category_master.update_category_master()

        # データ確認
        with conn.cursor() as cursor:
            sql = "SELECT * FROM category WHERE file_name = '{0}' ORDER BY category ".format(table)
            cursor.execute(sql)
            results = cursor.fetchall()
            self.assertEqual(len(results),5)
            self.assertEqual(results[0]['category'],'update_category_masterテスト1カテゴリ')
            self.assertEqual(results[1]['category'],'update_category_masterテスト2カテゴリ')
            self.assertEqual(results[2]['category'],'update_category_masterテスト3カテゴリ')
            self.assertEqual(results[3]['category'],'update_category_masterテスト4カテゴリ')
            self.assertEqual(results[4]['category'],'update_category_masterテスト5カテゴリ')
            # コミット
            conn.commit()

        with conn.cursor() as cursor:
            # 終わったらテストデータ削除
            sql = "DELETE FROM {0} ".format(table)
            cursor.execute(sql)
            sql = "DELETE FROM category WHERE file_name = '{0}' ".format(table)
            cursor.execute(sql)

        # 全て成功したらコミット
        conn.commit()
        conn.close()

    # カテゴリマスタ入れ替えのテスト
    def test_replace_category_master(self):

        # 入力データ
        input_data = "\n".join(["update_category_masterテスト1問題,update_category_masterテスト1答え,update_category_masterテスト1カテゴリ,update_category_masterテスト1画像"
                                ,"update_category_masterテスト2問題,update_category_masterテスト2答え,update_category_masterテスト2カテゴリ,update_category_masterテスト2画像"
                                ,"update_category_masterテスト3問題,update_category_masterテスト3答え,update_category_masterテスト3カテゴリ,update_category_masterテスト3画像"])
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

        # カテゴリマスタ追加
        update_category_master.update_category_master()

        # データ確認
        with conn.cursor() as cursor:
            sql = "SELECT * FROM category WHERE file_name = '{0}' ORDER BY category ".format(table)
            cursor.execute(sql)
            results = cursor.fetchall()
            self.assertEqual(len(results),3)
            self.assertEqual(results[0]['category'],'update_category_masterテスト1カテゴリ')
            self.assertEqual(results[1]['category'],'update_category_masterテスト2カテゴリ')
            self.assertEqual(results[2]['category'],'update_category_masterテスト3カテゴリ')

            # 確認したら、一回テストデータは削除する
            sql = "DELETE FROM {0} ".format(table)
            cursor.execute(sql)
            # コミット
            conn.commit()


        # 入力データその２
        input_data = "\n".join(["update_category_masterテスト4問題,update_category_masterテスト4答え,update_category_masterテスト4カテゴリ,update_category_masterテスト4画像"
                                ,"update_category_masterテスト5問題,update_category_masterテスト5答え,update_category_masterテスト5カテゴリ,update_category_masterテスト5画像"])

        # データその２を追加
        add_quiz.add_quiz(file_num,input_data)

        # カテゴリマスタ更新
        update_category_master.update_category_master()

        # データ確認（入力データその２　カテゴリのみになっているか）
        with conn.cursor() as cursor:
            sql = "SELECT * FROM category WHERE file_name = '{0}' ORDER BY category ".format(table)
            cursor.execute(sql)
            results = cursor.fetchall()
            self.assertEqual(len(results),2)
            self.assertEqual(results[0]['category'],'update_category_masterテスト4カテゴリ')
            self.assertEqual(results[1]['category'],'update_category_masterテスト5カテゴリ')
            # コミット
            conn.commit()

        with conn.cursor() as cursor:
            # 終わったらテストデータ削除
            sql = "DELETE FROM {0} ".format(table)
            cursor.execute(sql)
            sql = "DELETE FROM category WHERE file_name = '{0}' ".format(table)
            cursor.execute(sql)

        # 全て成功したらコミット
        conn.commit()
        conn.close()



if __name__ == '__main__':
    unittest.main()
