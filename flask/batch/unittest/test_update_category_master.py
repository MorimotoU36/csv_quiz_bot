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
from ini import get_messages_ini

from ut_common import delete_all_quiz_of_file

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

        # データ編集
        update_category_master.update_category_master()

        # データ確認
        with conn.cursor() as cursor:
            sql = "SELECT * FROM category WHERE file_num = {0} ORDER BY category ".format(file_num)
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

        # 終わったらテストデータ削除
        self.assertEqual(delete_all_quiz_of_file(conn,file_num),0)

        with conn.cursor() as cursor:
            # 終わったらテストデータ削除
            sql = "DELETE FROM category WHERE file_num = {0} ".format(file_num)
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

        # カテゴリマスタ追加
        update_category_master.update_category_master()

        # データ確認
        with conn.cursor() as cursor:
            sql = "SELECT * FROM category WHERE file_num = {0} ORDER BY category ".format(file_num)
            cursor.execute(sql)
            results = cursor.fetchall()
            self.assertEqual(len(results),3)
            self.assertEqual(results[0]['category'],'update_category_masterテスト1カテゴリ')
            self.assertEqual(results[1]['category'],'update_category_masterテスト2カテゴリ')
            self.assertEqual(results[2]['category'],'update_category_masterテスト3カテゴリ')

            # 終わったらテストデータ削除
            self.assertEqual(delete_all_quiz_of_file(conn,file_num),0)
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
            sql = "SELECT * FROM category WHERE file_num = {0} ORDER BY category ".format(file_num)
            cursor.execute(sql)
            results = cursor.fetchall()
            self.assertEqual(len(results),2)
            self.assertEqual(results[0]['category'],'update_category_masterテスト4カテゴリ')
            self.assertEqual(results[1]['category'],'update_category_masterテスト5カテゴリ')
            # コミット
            conn.commit()

        # 終わったらテストデータ削除
        self.assertEqual(delete_all_quiz_of_file(conn,file_num),0)

        with conn.cursor() as cursor:
            # 終わったらテストデータ削除
            sql = "DELETE FROM category WHERE file_num = {0} ".format(file_num)
            cursor.execute(sql)

        # 全て成功したらコミット
        conn.commit()
        conn.close()



if __name__ == '__main__':
    unittest.main()
