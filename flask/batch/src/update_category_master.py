# -*- coding: utf-8 -*-
import os
import sys
import traceback
import pymysql
import pymysql.cursors

sys.path.append(os.path.join(os.path.dirname(__file__), '../module'))
from dbconfig import get_connection
from ini import get_table_list, get_messages_ini

def update_category_master():
    """問題ファイルからカテゴリを取得しマスタに登録する関数

    Args:
        なし

    Returns:
        なし
    """

    # 設定ファイルを呼び出してファイル番号からテーブル名を取得
    # (変なファイル番号ならエラー終了)
    messages = get_messages_ini()
    table_list = get_table_list()
    try:
        table = [ table_list[i]['name'] for i in range (len(table_list)) ]
        nickname = [ table_list[i]['nickname'] for i in range (len(table_list)) ]
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

    # SQLを作成して投げる
    try:
        # 追加するカテゴリ数
        insert_categories = 0

        with conn.cursor() as cursor:
            # カテゴリマスタのデータを全削除
            sql_statement = "DELETE FROM category "
            cursor.execute(sql_statement)
            results = cursor.fetchall()

            # テーブル毎にカテゴリのリストを取得してマスタに更新
            for i in range(len(table)):
                # 問題テーブルからカテゴリのリストを取得
                sql_statement = "SELECT DISTINCT category FROM {0} WHERE deleted != 1 ".format(table[i])
                cursor.execute(sql_statement)
                results = cursor.fetchall()

                categories = set([])
                for ri in results:
                    categories = categories | set(list(ri['category'].split(':')))

                # カテゴリマスタにデータを入れる
                for ci in categories:
                    sql_statement = "INSERT INTO category VALUES('{0}','{1}') ".format(table[i],ci)
                    cursor.execute(sql_statement)
                insert_categories += len(categories)
        
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

    # 結果をJSONに変形して返す
    return {
        "statusCode": 200,
        "message": "カテゴリマスタの更新が完了しました（カテゴリ数：{0}）".format(insert_categories),
    }

if __name__=="__main__":
    print('update_category_master!')
