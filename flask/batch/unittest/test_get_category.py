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
from dbconfig import get_connection, get_file_info
from ini import get_messages_ini

from ut_common import delete_all_quiz_of_file

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

        # 終わったらテストデータ削除
        self.assertEqual(delete_all_quiz_of_file(conn,file_num),0)

        # 全て成功したらコミット
        conn.commit()
        conn.close()

if __name__ == '__main__':
    unittest.main()