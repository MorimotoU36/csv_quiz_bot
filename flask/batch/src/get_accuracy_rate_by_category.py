# -*- coding: utf-8 -*-
import os
import sys
import traceback
import pymysql
import pymysql.cursors

sys.path.append(os.path.join(os.path.dirname(__file__), '../module'))
from dbconfig import get_connection
from ini import get_table_list

def get_accuracy_rate_by_category(file_ind):
    """ファイル番号からカテゴリ毎の正解率を取得する関数

    Args:
        file_ind (int): ファイル番号

        Returns:
            result [JSON]: 取得した結果のリスト
    """

    # 設定ファイルを呼び出してファイル番号からテーブル名を取得
    # (変なファイル番号ならエラー終了)
    try:
        table_list = get_table_list()
        table = table_list[file_ind]['name']
        nickname = table_list[file_ind]['nickname']
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

    # # SQLを作成して投げる
    try:
        with conn.cursor() as cursor:
            # 検索語句がカテゴリに含まれる
            # SQLを実行する
            sql_statement = "SELECT c_category,accuracy_rate FROM {0} ORDER BY accuracy_rate ".format(table+'_category_view')
            cursor.execute(sql_statement)

            # MySQLから帰ってきた結果を受け取る
            # Select結果を取り出す
            results = cursor.fetchall()
            # TODO Decimal -> strに直す効率良い方法、もしくは数値のままでもエラー出ずに返せる方法（DecimalのままだとAPIで取得時にエラーになる）
            for i in range(len(results)):
                ri = results[i]
                ri['accuracy_rate'] = str(ri['accuracy_rate'])
                results[i] = ri

            # (追加機能)カテゴリとは別に、チェック済の問題だけの正解率を計算して出す
            sql_statement = "SELECT checked, SUM(clear_count) as sum_clear, SUM(fail_count) as sum_fail, ( SUM(clear_count) / ( SUM(clear_count) + SUM(fail_count) ) ) as accuracy_rate FROM {0} where checked = 1 group by checked;".format(table+"_view")
            cursor.execute(sql_statement)
            checked_result = cursor.fetchall()
            # Decimal -> str変換
            for cri in checked_result:
                cri['sum_clear'] = str(cri['sum_clear'])
                cri['sum_fail'] = str(cri['sum_fail'])
                cri['accuracy_rate'] = str(cri['accuracy_rate'])

        # 結果をJSONに変形して返す
        return {
            "statusCode": 200,
            "result": results,
            "checked_result": checked_result
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "message": 'Error: DB操作時にエラーが発生しました',
            "traceback": traceback.format_exc()
        }


if __name__=="__main__":
    res = get_accuracy_rate_by_category(0)
    print(res)