# -*- coding: utf-8 -*-
import os
import sys
import traceback
import pymysql
import pymysql.cursors

sys.path.append(os.path.join(os.path.dirname(__file__), '../module'))
from dbconfig import get_connection, get_file_info
from ini import get_messages_ini

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

    # メッセージ設定ファイルを呼び出す
    messages = get_messages_ini()

    # 入力内容確認
    if (question is None or len(question.strip())==0) and (answer is None or len(answer.strip())==0) and (category is None or len(category.strip())==0) and (img_file is None or len(img_file.strip())==0):
        return {
            "statusCode": 500,
            "message": messages['ERR_0006']
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
        # 入力内容からSQLを作成して投げる
        # SQLを実行する
        with conn.cursor() as cursor:
            # テーブルに入力内容を更新する
            update_question = "" if question is None or len(question.strip())==0 else " quiz_sentense = '{0}', ".format(question)
            update_answer   = "" if answer is None or len(answer.strip())==0 else " answer = '{0}', ".format(answer)
            update_category = "" if category is None or len(category.strip())==0 else " category = '{0}', ".format(category)
            update_img_file = " img_file = '' " if img_file is None else " img_file = '{0}' ".format(img_file)
            sql = "UPDATE quiz SET {0} {1} {2} {3} WHERE file_num = {4} AND quiz_num = {5} ".format(update_question,update_answer,update_category,update_img_file,file_num,quiz_num)
            cursor.execute(sql)

            result = "Success!! [{0}-{1}]:{2},{3},{4},{5}".format(nickname,str(quiz_num),question,answer,category,img_file)

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

    # 設定値取得
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

    try:
        # data内のクエリを１個１個見ていく
        for data_i in data:
            # ファイル番号を取得
            file_num = data_i['file_num']
            # 問題番号を取得
            quiz_num = data_i['quiz_num']
            # 追加・削除するカテゴリを取得
            query_category = data_i['category']

            # ファイル番号からテーブル名を取得
            table_info = get_file_info(conn,file_num)
            if(table_info['statusCode'] == 200):
                nickname = table_info['result']['file_nickname']
            else:
                return {
                    "statusCode": 400,
                    "message": messages['ERR_0001']
                }

            with conn.cursor() as cursor:
                # まずは問題を取得
                sql = "SELECT file_num, quiz_num, quiz_sentense, answer, clear_count, fail_count, category, img_file FROM quiz WHERE file_num = {0} AND quiz_num = {1}".format(file_num,quiz_num)
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
                sql = "UPDATE quiz SET category = '{0}' WHERE file_num = {1} AND quiz_num = {2} ".format(category,file_num,quiz_num)
                cursor.execute(sql)
        
        #全て成功したらコミット
        conn.commit()
        conn.close()

        return {
            "statusCode": 200,
            "message": "All OK."
        }

    except IndexError:
        return {
            "statusCode": 500,
            "message": messages['ERR_0001']
        }
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

    # 設定ファイルを呼び出す
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

    try:
        # data内のクエリを１個１個見ていく
        checked_i=[]
        unchecked_i=[]
        for data_i in data:
            # ファイル番号を取得
            file_num = data_i['file_num']
            # 問題番号を取得
            quiz_num = data_i['quiz_num']

            # ファイル番号からテーブル名を取得
            table_info = get_file_info(conn,file_num)
            if(table_info['statusCode'] == 200):
                nickname = table_info['result']['file_nickname']
            else:
                return {
                    "statusCode": 400,
                    "message": messages['ERR_0001']
                }

            with conn.cursor() as cursor:
                # まずは問題を取得
                sql = "SELECT checked FROM quiz WHERE file_num = {0} AND quiz_num = {1}".format(file_num,quiz_num)
                cursor.execute(sql)

                # MySQLから帰ってきた結果を受け取る
                # Select結果を取り出す
                results = cursor.fetchall()

                # チェック状態を取得
                checked = int(results[0]['checked'])

                # チェック状態を修正する
                if(checked == 0):
                    # チェックなしならチェックありにする
                    sql = "UPDATE quiz SET checked = {0} WHERE file_num = {1} AND quiz_num = {2} ".format(1,file_num,quiz_num)
                    cursor.execute(sql)
                    checked_i.append(str(quiz_num))
                else:
                    # チェックありならチェックなしにする
                    sql = "UPDATE quiz SET checked = {0} WHERE file_num = {1} AND quiz_num = {2} ".format(0,file_num,quiz_num)
                    cursor.execute(sql)
                    unchecked_i.append(str(quiz_num))

        #全て成功したらコミット
        conn.commit()
        conn.close()

        #チェック登録解除した問題のメッセージを作成
        message=""
        if(len(checked_i)>0):
            message+="checked to [" + ','.join(checked_i) + "] OK. "
        if(len(unchecked_i)>0):
            message+="unchecked to [" + ','.join(unchecked_i) + "] OK. "

        return {
            "statusCode": 200,
            "message": message
        }

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



if __name__=="__main__":
    print("edit_quiz!")