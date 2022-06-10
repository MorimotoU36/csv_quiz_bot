# -*- coding: utf-8 -*-
import os
import sys
import traceback
import pymysql
import pymysql.cursors

sys.path.append(os.path.join(os.path.dirname(__file__), '../module'))
from dbconfig import get_connection, get_file_info
from ini import get_messages_ini

def update_category_master():
    """問題ファイルからカテゴリを取得しマスタに登録する関数

    Args:
        なし

    Returns:
        なし
    """

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

    # SQLを作成して投げる
    try:
        # 追加するカテゴリ数
        insert_categories = 0

        with conn.cursor() as cursor:
            # ファイル情報取得
            sql_statement = "SELECT file_num, file_name, file_nickname FROM quiz_file"
            cursor.execute(sql_statement)
            table_info = cursor.fetchall()

            # カテゴリマスタのデータを全削除
            sql_statement = "DELETE FROM category "
            cursor.execute(sql_statement)
            results = cursor.fetchall()

            # テーブル毎にカテゴリのリストを取得してマスタに更新
            for i in range(len(table_info)):
                # 問題テーブルからカテゴリのリストを取得
                sql_statement = "SELECT DISTINCT category FROM quiz WHERE file_num = {0} AND deleted != 1 ".format(table_info[i]['file_num'])
                cursor.execute(sql_statement)
                results = cursor.fetchall()

                categories = set([])
                for ri in results:
                    categories = categories | set(list(ri['category'].split(':')))

                # カテゴリマスタにデータを入れる
                for ci in categories:
                    sql_statement = "INSERT INTO category VALUES('{0}','{1}') ".format(table_info[i]['file_num'],ci)
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
