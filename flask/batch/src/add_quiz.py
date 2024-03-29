# -*- coding: utf-8 -*-
import os
import sys
import traceback
import pymysql
import pymysql.cursors

sys.path.append(os.path.join(os.path.dirname(__file__), '../module'))
from dbconfig import get_connection, get_file_info
from ini import get_messages_ini

def add_quiz(file_num,input_data):
    """問題を追加する関数

    Args:
        file_num (int): ファイル番号
        input_data (str): 入力されたデータ(テスト問題,正解,カテゴリ,画像ファイル名)*x行（<-改行区切り）

        Returns:
            result (JSON): 取得した問題
    """

    # 入力データを１行ずつに分割
    input_data = list(input_data.split('\n'))

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

    try:
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
            new_quiz_id = -1
            with conn.cursor() as cursor:
                # 削除済問題がある場合はその番号に入れる
                sql = "SELECT quiz_num FROM quiz WHERE file_num = {0} AND deleted = 1 ORDER BY quiz_num LIMIT 1 ".format(file_num)
                cursor.execute(sql)
                sql_results = cursor.fetchall()

            if(len(sql_results) > 0):
                new_quiz_id = sql_results[0]['quiz_num']
                # 削除済問題のところにデータを更新する形でいれる
                with conn.cursor() as cursor:
                    sql = "UPDATE quiz SET quiz_sentense = '{0}', answer = '{1}', clear_count = 0, fail_count = 0, category = '{2}', img_file = '{3}', checked = 0, deleted = 0 WHERE file_num = {4} AND quiz_num = {5} ".format(question,answer,category,img_file,file_num,new_quiz_id)
                    cursor.execute(sql)

                    result.append("Added!! [{0}-{1}]:{2},{3}".format(nickname,str(new_quiz_id),question,answer))

            else:
                # 削除済問題がない場合
                # データ全件数から番号を決定する
                with conn.cursor() as cursor:
                    # 指定したテーブルの件数を調べる
                    sql = "SELECT count(*) FROM quiz WHERE file_num = {0}".format(file_num)
                    cursor.execute(sql)
                    results = cursor.fetchall()
                    new_quiz_id = results[0]['count(*)']
                    new_quiz_id += 1

                # テーブル名と問題番号からSQLを作成して投げる
                # (問題番号が範囲外なら終了)
                # SQLを実行する
                with conn.cursor() as cursor:
                    # データを挿入する
                    sql = "INSERT INTO quiz VALUES({0},{1},'{2}','{3}',0,0,'{4}','{5}',0,0)".format(file_num,new_quiz_id,question,answer,category,img_file)
                    cursor.execute(sql)

                    result.append("Added!! [{0}-{1}]:{2},{3}".format(nickname,str(new_quiz_id),question,answer))

        else:
            #全て成功したらコミット
            conn.commit()
            conn.close()

    # DB操作失敗時はロールバック
    except Exception as e:
        message = messages['ERR_0004']
        try:
            conn.rollback()
        except:
            message = messages['ERR_0005']
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
    print("add_quiz!")
