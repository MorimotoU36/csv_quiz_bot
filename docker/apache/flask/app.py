# -*- coding: utf-8 -*-
import traceback
from batch.src.select_quiz import select_quiz
from batch.src.random_quiz import random_quiz

from flask import Flask, request
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

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
        return result
    except Exception as e:
        return traceback.format_exc()
        return {
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
        return result
    except Exception as e:
        return traceback.format_exc()
        return {
            "error" : traceback.format_exc()
        }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4999, debug=True)