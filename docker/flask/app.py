# -*- coding: utf-8 -*-
import json
import traceback
from batch.src.select_quiz import select_quiz
from batch.src.random_quiz import random_quiz
from batch.src.worst_quiz import worst_quiz
from batch.src.answer_inputter import answer_input
from batch.src.search_quiz import search_quiz
from batch.src.minimum_quiz import minimum_quiz
from batch.module.ini import get_table_list

from flask import Flask, request
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return 'Hello, Flask!'

@app.route('/select', methods=["POST"])
def select():
    """問題取得API
    Args: JSON
    {
        "file_num": ファイル番号,
        "quiz_num": 問題番号,
        "image_flag": 画像取得フラグ 
    }

    Returns:
        [type]: [description]
    """
    try:
        # リクエストから値を読み取る
        req = request.json
        file_num = int(req.get("file_num"))
        quiz_num = int(req.get("quiz_num"))
        image_flag = bool(req.get("image"))

        # MySQLに問題を取得しにいく
        result = select_quiz(file_num,quiz_num,image_flag)

        # 取得結果を返す
        return {
            "statusCode" : 200,
            "response" : result
        }
    except Exception as e:
        return traceback.format_exc()
        return {
            "statusCode" : 500,
            "error" : traceback.format_exc()
        }

@app.route('/random', methods=["POST"])
def random():
    """ランダム問題取得API
    Args: JSON
    {
        "file_num": ファイル番号(オプション),
        "image": 画像取得フラグ(オプション),
        "rate": 正解率(オプション)
    }

    Returns:
        result(JSON): 取得した問題またはエラーログ
    """
    try:
        # リクエストから値を読み取る。ない場合はデフォルト値
        req = request.json
        file_num = int(req.get("file_num",-1))
        image_flag = bool(req.get("image",True))
        rate = float(req.get("rate",100))

        # MySQLに問題を取得しにいく
        result = random_quiz(file_num=file_num,image=image_flag,rate=rate)

        # 取得結果を返す
        return {
            "statusCode" : 200,
            "response" : result
        }
    except Exception as e:
        return traceback.format_exc()
        return {
            "statusCode" : 500,
            "error" : traceback.format_exc()
        }

@app.route('/worst_rate', methods=["POST"])
def worst():
    """最低正解率問題取得API
    Args: JSON
    {
        "file_num": ファイル番号(オプション),
        "category": カテゴリ(オプション)
        "image": 画像取得フラグ(オプション),
    }

    Returns:
        result(JSON): 取得した問題またはエラーログ
    """
    try:
        # リクエストから値を読み取る。ない場合はデフォルト値
        req = request.json
        file_num = int(req.get("file_num",-1))
        category = req.get("category",None)
        image_flag = bool(req.get("image",True))

        # MySQLに問題を取得しにいく
        result = worst_quiz(file_num=file_num,category=category,image=image_flag)

        # 取得結果を返す
        return result
    except Exception as e:
        return {
            "error" : traceback.format_exc()
        }

@app.route('/answer', methods=["POST"])
def answer():
    """解答登録API
    Args: JSON
    {
        "file_num": ファイル番号
        "quiz_num": 問題番号
        "clear": 正解ならTrue、不正解ならFalse
    }

    Returns:
        result: 成功またはエラーログ
    """
    try:
        # リクエストから値を読み取る
        req = request.json
        file_num = int(req.get("file_num"))
        quiz_num = int(req.get("quiz_num"))
        clear = bool(req.get("clear"))

        # MySQLに問題を取得しにいく
        result = answer_input(file_num,quiz_num,clear)

        # 取得結果を返す
        return {
            "statusCode" : 200,
            "req" : req,
            "result" : result
        }
    except Exception as e:
        return {
            "statusCode" : 500,
            "error" : traceback.format_exc()
        }

@app.route('/search', methods=["POST"])
def search():
    """問題検索API
    Args: JSON
    {
        "query": 検索語句
        "file_num": ファイル番号
    }

    Returns:
        result(JSON): 成功またはエラーログ
    """
    try:
        # リクエストから値を読み取る。
        req = request.json
        file_num = int(req.get("file_num"))
        query = req.get("query","")
    
        # MySQLに問題を取得しにいく
        result = search_quiz(query,file_num)

        # 取得結果を返す
        return {
            "req" : req,
            "result" : result
        }
    except Exception as e:
        return {
            "error" : traceback.format_exc()
        }

@app.route('/minimum', methods=["POST"])
def minimum():
    """最小正解数問題取得API
    Args: JSON
    {
        "file_num": ファイル番号(オプション),
        "category": カテゴリ(オプション)
        "image": 画像取得フラグ(オプション),
    }

    Returns:
        result(JSON): 取得した問題またはエラーログ
    """
    try:
        # リクエストから値を読み取る。ない場合はデフォルト値
        req = request.json
        file_num = int(req.get("file_num",-1))
        category = req.get("category",None)
        image_flag = bool(req.get("image",True))

        # MySQLに問題を取得しにいく
        result = worst_quiz(file_num=file_num,category=category,image=image_flag)

        # 取得結果を返す
        return result
    except Exception as e:
        return {
            "error" : traceback.format_exc()
        }

@app.route('/namelist', methods=["POST"])
def namelist():
    """問題ファイル名取得API
    Args: なし

    Returns:
        [JSON] : { 'table' : テーブル名のリスト }
    """
    try:
        # テーブル名のリストを(JSON形式で)返す
        return { 
            'statusCode' : 200,
            'table' : get_table_list() 
        }
    except Exception as e:
        return {
            'statusCode' : 500,
            "error" : traceback.format_exc()
        }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4999, debug=True)