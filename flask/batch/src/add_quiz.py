# -*- coding: utf-8 -*-
import os
import sys
import traceback
import pymysql
import pymysql.cursors

sys.path.append(os.path.join(os.path.dirname(__file__), '../module'))
from dbconfig import get_connection
from ini import get_table_list

def add_quiz(file_num,input_data):
    """ファイル番号、問題番号、イメージ取得フラグから問題を取得する関数

    Args:
        file_num (int): ファイル番号
        input_data (str): 入力されたデータ(テスト問題,正解,カテゴリ,画像ファイル名)*x行

        Returns:
            result (JSON): 取得した問題
    """

    # 入力データを１行ずつに分割
    input_data = list(input_data.split('\n'))

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

    try:
        # データ全件数を確認
        count = 0
        with conn.cursor() as cursor:
            # 指定したテーブルの件数を調べる
            sql = "SELECT count(*) FROM {0}".format(table)
            cursor.execute(sql)
            results = cursor.fetchall()
            count = results[0]['count(*)']

        # 返るデータ
        result = []

        # １行ずつ処理し、全て正常に行えた場合のみコミット、途中でエラーが発生した場合はロールバック
        for di in input_data:

            # 入力データ作成
            data_i = di.split(',')
            question = data_i[0]
            answer = data_i[1]
            category = data_i[2]
            img_file = data_i[3]

            # データのidを作成
            count += 1

            # テーブル名と問題番号からSQLを作成して投げる
            # (問題番号が範囲外なら終了)
            # SQLを実行する
            with conn.cursor() as cursor:
                # データを挿入する
                sql = "INSERT INTO {0} VALUES({1},'{2}','{3}',0,0,'{4}','{5}',0)".format(table,count,question,answer,category,img_file)
                print(sql)
                cursor.execute(sql)

                result.append("Added!! [{0}-{1}]:{2},{3}".format(nickname,str(count),question,answer))

        else:
            #全て成功したらコミット
            conn.commit()
            conn.close()

    # DB操作失敗時はロールバック
    except Exception as e:
        message = 'Error: DB操作時にエラーが発生しました '
        try:
            conn.rollback()
        except:
            message += '( ロールバックにも失敗しました )'
        finally:
            return {
                "statusCode": 500,
                "message": message,
                "traceback": traceback.format_exc()
            }

    # 結果(文字列)を返す
    return {
        "statusCode": 200,
        "result": result
    }

if __name__=="__main__":
    res = add_quiz(2,"data1,data2,,\ndata5,data6,data7,data8")
    print(res)