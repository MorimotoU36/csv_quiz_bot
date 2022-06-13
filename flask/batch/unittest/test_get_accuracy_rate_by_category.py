# -*- coding: utf-8 -*-
import os
import sys
import time
import traceback
import pymysql
import pymysql.cursors

import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
import get_accuracy_rate_by_category
import update_category_master
import add_quiz

sys.path.append(os.path.join(os.path.dirname(__file__), '../module'))
from dbconfig import get_connection, get_file_info
from ini import get_messages_ini

from ut_common import delete_all_quiz_of_file

class TestGetAccuracyRateByCategory(unittest.TestCase):

    # 問題を1つ編集するテスト
    def test_get_accuracy_rate_by_category(self):
        # 入力データ
        input_data = "\n".join(["get_accuracy_rate_by_categoryテスト1問題,get_accuracy_rate_by_categoryテスト1答え,get_accuracy_rate_by_categoryテスト1カテゴリ,get_accuracy_rate_by_categoryテスト1画像"
                                ,"get_accuracy_rate_by_categoryテスト2問題,get_accuracy_rate_by_categoryテスト2答え,get_accuracy_rate_by_categoryテスト2カテゴリ,get_accuracy_rate_by_categoryテスト2画像"
                                ,"get_accuracy_rate_by_categoryテスト3問題,get_accuracy_rate_by_categoryテスト3答え,get_accuracy_rate_by_categoryテスト3カテゴリ,get_accuracy_rate_by_categoryテスト3画像"
                                ,"get_accuracy_rate_by_categoryテスト4問題,get_accuracy_rate_by_categoryテスト4答え,get_accuracy_rate_by_categoryテスト4カテゴリ,get_accuracy_rate_by_categoryテスト4画像"
                                ,"get_accuracy_rate_by_categoryテスト5問題,get_accuracy_rate_by_categoryテスト5答え,get_accuracy_rate_by_categoryテスト5カテゴリ,get_accuracy_rate_by_categoryテスト5画像"])
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

        # カテゴリマスタ更新
        update_category_master.update_category_master()

        # データ取得
        response = get_accuracy_rate_by_category.get_accuracy_rate_by_category(file_num)
        results = []
        for ri in response['result']:
            results.append([ri['c_category'],ri['count']])
        results.sort(key=lambda x: x[0])

        self.assertEqual(len(results),5)
        self.assertEqual(results[0][0],'get_accuracy_rate_by_categoryテスト1カテゴリ')
        self.assertEqual(results[1][0],'get_accuracy_rate_by_categoryテスト2カテゴリ')
        self.assertEqual(results[2][0],'get_accuracy_rate_by_categoryテスト3カテゴリ')
        self.assertEqual(results[3][0],'get_accuracy_rate_by_categoryテスト4カテゴリ')
        self.assertEqual(results[4][0],'get_accuracy_rate_by_categoryテスト5カテゴリ')

        with conn.cursor() as cursor:
            # 終わったらテストデータ削除
            sql = "DELETE FROM quiz WHERE file_num = {0} ".format(file_num)
            cursor.execute(sql)
            sql = "DELETE FROM category WHERE file_num = {0} ".format(file_num)
            cursor.execute(sql)

        # 全て成功したらコミット
        conn.commit()
        conn.close()

if __name__ == '__main__':
    unittest.main()

