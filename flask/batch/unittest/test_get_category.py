# -*- coding: utf-8 -*-
import os
import sys
import time
import traceback
import pymysql
import pymysql.cursors

import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
import get_category
import add_quiz

sys.path.append(os.path.join(os.path.dirname(__file__), '../module'))
from dbconfig import get_connection
from ini import get_table_list, get_messages_ini

class TestGetCategory(unittest.TestCase):

    # カテゴリを取ってくるテスト
    def test_get_category(self):

        # 入力データ
        input_data = "\n".join(["get_categoryテスト1問題,get_categoryテスト1答え,get_categoryテスト1カテゴリ,get_categoryテスト1画像"
                                ,"get_categoryテスト2問題,get_categoryテスト2答え,get_categoryテスト2カテゴリ,get_categoryテスト2画像"
                                ,"get_categoryテスト3問題,get_categoryテスト3答え,get_categoryテスト3カテゴリ,get_categoryテスト3画像"
                                ,"get_categoryテスト4問題,get_categoryテスト4答え,get_categoryテスト4カテゴリ,get_categoryテスト4画像"
                                ,"get_categoryテスト5問題,get_categoryテスト5答え,get_categoryテスト5カテゴリ,get_categoryテスト5画像"])
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

        # データ取得
        response = get_category.get_category(file_num)
        self.assertEqual(response['statusCode'],200)
        result = response['result']
        result.sort()

        self.assertEqual(len(result),5)
        self.assertEqual(result[0],'get_categoryテスト1カテゴリ')
        self.assertEqual(result[1],'get_categoryテスト2カテゴリ')
        self.assertEqual(result[2],'get_categoryテスト3カテゴリ')
        self.assertEqual(result[3],'get_categoryテスト4カテゴリ')
        self.assertEqual(result[4],'get_categoryテスト5カテゴリ')

        with conn.cursor() as cursor:
            # 終わったらテストデータ削除
            sql = "DELETE FROM {0} ".format(table)
            cursor.execute(sql)

        # 全て成功したらコミット
        conn.commit()
        conn.close()

if __name__ == '__main__':
    unittest.main()