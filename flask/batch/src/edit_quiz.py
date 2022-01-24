# -*- coding: utf-8 -*-
import os
import sys
import traceback
import pymysql
import pymysql.cursors

sys.path.append(os.path.join(os.path.dirname(__file__), '../module'))
from dbconfig import get_connection
from ini import get_table_list

def edit_quiz(file_num,quiz_num,question,answer,category,img_file):
    """入力データで問題を編集する関数

    Args:
        file_num (int): ファイル番号
        quiz_num (int): 問題番号
        question (str): 問題文
        answer (str): 答えの文
        category (str): カテゴリ
        img_file (str): 画像ファイル名

    Returns:
        [type]: [description]
    """

    # 入力内容確認
    if (question is None or len(question.strip())==0) and (answer is None or len(answer.strip())==0) and (category is None or len(category.strip())==0) and (img_file is None or len(img_file.strip())==0):
        return {
            "statusCode": 500,
            "message": 'Error: 入力内容がありません'
        }

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
        # 入力内容からSQLを作成して投げる
        # SQLを実行する
        with conn.cursor() as cursor:
            # テーブルに入力内容を更新する
            update_question = "" if question is None or len(question.strip())==0 else " quiz_sentense = '{0}', ".format(question)
            update_answer   = "" if answer is None or len(answer.strip())==0 else " answer = '{0}', ".format(answer)
            update_category = "" if category is None or len(category.strip())==0 else " category = '{0}', ".format(category)
            update_img_file = " img_file = '' " if img_file is None else " img_file = '{0}' ".format(img_file)
            sql = "UPDATE {0} SET {1} {2} {3} {4} WHERE quiz_num = {5} ".format(table,update_question,update_answer,update_category,update_img_file,quiz_num)
            print(sql)
            cursor.execute(sql)

            result = "Success!! [{0}-{1}]:{2},{3},{4},{5}".format(nickname,str(quiz_num),question,answer,category,img_file)

        #全て成功したらコミット
        conn.commit()
        conn.close()

    # DB操作失敗時はロールバック
    except Exception as e:
        message = 'Error: DB接続時にエラーが発生しました '
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

def edit_category_of_question(data):
    """問題にカテゴリを追加・削除する関数

    Args:
        data ([JSON]): JSONの配列
        要素は
        {
            "file_num" : ファイル番号(int)
            "quiz_num" : 問題番号(int)
            "category" : 追加・削除するカテゴリ
        }
    """

    # テーブルリスト取得
    table_list = get_table_list()

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
        # data内のクエリを１個１個見ていく
        for data_i in data:
            # ファイル番号を取得
            file_num = data_i['file_num']
            # 問題番号を取得
            quiz_num = data_i['quiz_num']
            # 追加・削除するカテゴリを取得
            query_category = data_i['category']

            # テーブル名取得
            table = table_list[file_num]['name']
            nickname = table_list[file_num]['nickname']

            with conn.cursor() as cursor:
                # まずは問題を取得
                sql = "SELECT quiz_num, quiz_sentense, answer, clear_count, fail_count, category, img_file FROM {0} WHERE quiz_num = {1}".format(table,quiz_num)
                cursor.execute(sql)

                # MySQLから帰ってきた結果を受け取る
                # Select結果を取り出す
                results = cursor.fetchall()

                # カテゴリを取得
                category = results[0]['category']

                # カテゴリを修正する
                if(category is not None and query_category in category):
                    # クエリで出したカテゴリがすでにある場合はそれを削除する
                    category = category.replace(query_category,"")
                    category = category.replace("::",":")
                    if(category == ":"):
                        category = ""
                    elif(len(category)>1 and category[0]==":"):
                        category = category[1:]
                    elif(len(category)>1 and category[-1]==":"):
                        category = category[:-1]
                else:
                    # クエリで出したカテゴリが含まれてない場合は追加する
                    if(category is None or category == ''):
                        category = query_category
                    else:
                        category = category + ":" + query_category
                
                # アップデート
                sql = "UPDATE {0} SET category = '{1}' WHERE quiz_num = {2} ".format(table,category,quiz_num)
                cursor.execute(sql)
        
        #全て成功したらコミット
        conn.commit()
        conn.close()

        return {
            "statusCode": 200,
            "message": "All OK."
        }

    # DB操作失敗時はロールバック
    except Exception as e:
        message = 'Error: DB接続時にエラーが発生しました '
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



def edit_checked_of_question(data):
    """問題のチェックを変更する関数

    Args:
        data ([JSON]): JSONの配列
        要素は
        {
            "file_num" : ファイル番号(int)
            "quiz_num" : 問題番号(int)
        }
    """

    # テーブルリスト取得
    table_list = get_table_list()

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
        # data内のクエリを１個１個見ていく
        for data_i in data:
            # ファイル番号を取得
            file_num = data_i['file_num']
            # 問題番号を取得
            quiz_num = data_i['quiz_num']

            # テーブル名取得
            table = table_list[file_num]['name']
            nickname = table_list[file_num]['nickname']

            with conn.cursor() as cursor:
                # まずは問題を取得
                sql = "SELECT checked FROM {0} WHERE quiz_num = {1}".format(table,quiz_num)
                cursor.execute(sql)

                # MySQLから帰ってきた結果を受け取る
                # Select結果を取り出す
                results = cursor.fetchall()

                # チェック状態を取得
                checked = int(results[0]['checked'])
                print(checked)

                # チェック状態を修正する
                if(checked == 0):
                    # チェックなしならチェックありにする
                    sql = "UPDATE {0} SET checked = {1} WHERE quiz_num = {2} ".format(table,1,quiz_num)
                    cursor.execute(sql)
                else:
                    # チェックありならチェックなしにする
                    sql = "UPDATE {0} SET checked = {1} WHERE quiz_num = {2} ".format(table,0,quiz_num)
                    cursor.execute(sql)

        #全て成功したらコミット
        conn.commit()
        conn.close()

        return {
            "statusCode": 200,
            "message": "All OK."
        }

    # DB操作失敗時はロールバック
    except Exception as e:
        message = 'Error: DB接続時にエラーが発生しました '
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



if __name__=="__main__":
#    res = edit_quiz(2,99,"ques1","ans2","cat3","img4")
    # data = [
    #     {
    #         "file_num" : 2,
    #         "quiz_num" : 93,
    #         "category" : "テスト"
    #     },
    #     {
    #         "file_num" : 2,
    #         "quiz_num" : 94,
    #         "category" : "テスト"
    #     },
    #     {
    #         "file_num" : 2,
    #         "quiz_num" : 95,
    #         "category" : "テスト"
    #     }
    # ]
    # res = edit_category_of_question(data)
    data = [
        {
            "file_num" : 2,
            "quiz_num" : 93
        },
        {
            "file_num" : 2,
            "quiz_num" : 94
        },
        {
            "file_num" : 2,
            "quiz_num" : 95
        }
    ]
    res = edit_checked_of_question(data)
    print(res)