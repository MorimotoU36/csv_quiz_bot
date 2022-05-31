# -*- coding: utf-8 -*-
import os
import sys
import traceback
import pymysql
import pymysql.cursors

sys.path.append(os.path.join(os.path.dirname(__file__), '../module'))
from dbconfig import get_connection
from ini import get_table_list

def integrate_quiz(pre_file_num,pre_quiz_num,post_file_num,post_quiz_num):
    """入力データで問題を統合する関数

    Args:
        pre_file_num (int):  統合される問題のファイル番号
        pre_quiz_num (int):  統合される問題の問題番号
        post_file_num (int): 統合先の問題のファイル番号
        post_quiz_num (int): 統合先の問題番号

    Returns:
        [type]: [description]
    """

    # 統合前と先でファイル番号が違うなら終了（同じファイル間で統合できるようにする）
    if(pre_file_num != post_file_num):
        return {
            "statusCode": 400,
            "message": 'Error: 統合前と統合先の問題は同じファイルにして下さい'
        }

    # 設定ファイルを呼び出してファイル番号からテーブル名を取得
    # (変なファイル番号ならエラー終了)
    try:
        table_list = get_table_list()
        table = table_list[pre_file_num]['name']
        nickname = table_list[pre_file_num]['nickname']
    except IndexError:
        return {
            "statusCode": 400,
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
        with conn.cursor() as cursor:
            # 指定したテーブルの件数を調べる
            sql = "SELECT count(*) FROM {0}".format(table)
            cursor.execute(sql)
            results = cursor.fetchall()
            count = results[0]['count(*)']

            # 問題番号が範囲外なら終了
            if( (pre_quiz_num < 1 or count < pre_quiz_num) or (post_quiz_num < 1 or count < post_quiz_num) ):
                return {
                    "statusCode": 500,
                    "message": 'Error: {0}の問題番号は1~{1}の間で入力してください'.format(nickname,count)
                }

            # 統合される側の問題のデータを取得
            sql = "SELECT quiz_num, quiz_sentense, answer, clear_count, fail_count, category, img_file, checked, deleted FROM {0} WHERE quiz_num = {1}".format(table,pre_quiz_num)
            cursor.execute(sql)
            pre_results = cursor.fetchall()

            # 統合先の問題のデータを取得
            sql = "SELECT quiz_num, quiz_sentense, answer, clear_count, fail_count, category, img_file, checked, deleted FROM {0} WHERE quiz_num = {1}".format(table,post_quiz_num)
            cursor.execute(sql)
            post_results = cursor.fetchall()

            # 統合データ作成
            new_clear_count = int(pre_results[0]['clear_count']) + int(post_results[0]['clear_count'])
            new_fail_count  = int(pre_results[0]['fail_count']) + int(post_results[0]['fail_count'])
            new_category    = ':'.join(list(set(pre_results[0]['category'].split(':')) | set(post_results[0]['category'].split(':')) ))
            print(new_category)

            # 統合データ更新
            sql = "UPDATE {0} SET clear_count = {1}, fail_count = {2}, category = '{3}' WHERE quiz_num = {4} ".format(table,new_clear_count,new_fail_count,new_category,post_quiz_num)
            print(sql)
            cursor.execute(sql)

            # 統合元データ削除
            update_deleteflag = " deleted = 1 "
            sql = "UPDATE {0} SET {1} WHERE quiz_num = {2} ".format(table,update_deleteflag,pre_quiz_num)
            print(sql)
            cursor.execute(sql)

            result = "Success!! Integrated:[{0}:{1}->{2}] and deleted [{1}]".format(nickname,pre_quiz_num,post_quiz_num)

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

    print("integrate quiz test")
    # res = integrate_quiz(2,98,2,99)
    # print(res)