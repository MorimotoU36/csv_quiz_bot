# -*- coding: utf-8 -*-
import json
import traceback
from batch.src.select_quiz import select_quiz
from batch.src.random_quiz import random_quiz
from batch.src.worst_quiz import worst_quiz
from batch.src.answer_inputter import answer_input
from batch.src.search_quiz import search_quiz
from batch.src.minimum_quiz import minimum_quiz
from batch.src.add_quiz import add_quiz
from batch.src.edit_quiz import edit_quiz
from batch.module.ini import get_table_list
from batch.src.get_category import get_category
from batch.src.edit_quiz import edit_category_of_question
from batch.src.update_category_master import update_category_master
from batch.src.get_accuracy_rate_by_category import get_accuracy_rate_by_category
from batch.src.edit_quiz import edit_checked_of_question
from batch.src.s3_file_download import file_download

from flask import Flask, request
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return 'Hello, Django!'

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

        if(result['statusCode'] == 500):
            return {
                "statusCode" : 500,
                "error" : result["message"]
            }
        elif(len(result['result'])==0):
            return {
                "statusCode" : 404,
                "error" : "Not Found,指定された条件でのデータはありません(file_num:{0}, quiz_num:{1})".format(file_num,quiz_num)
            }
        else:
            # 取得結果を返す
            return {
                "statusCode" : 200,
                "response" : result['result'][0]
            }
    except Exception as e:
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
        "category": カテゴリ(オプション)
        "checked": チェック問題フラグ(オプション)
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
        category = req.get("category",'')
        checked = bool(req.get("checked",False))

        # MySQLに問題を取得しにいく
        result = random_quiz(file_num=file_num,image=image_flag,rate=rate,category=category,checked=checked)

        if(result['statusCode'] == 500):
            return {
                "statusCode" : 500,
                "error" : result["message"]
            }
        elif(len(result['result'])==0):
            return {
                "statusCode" : 404,
                "error" : "Not Found,指定された条件でのデータはありません(file_num:{0}, rate:{1}, category:{2}, checked:{3})".format(file_num,rate,category,checked)
            }
        else:
            # 取得結果を返す
            return {
                "statusCode" : 200,
                "response" : result['result'][0]
            }
    except Exception as e:
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
        "checked": チェック問題フラグ(オプション)
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
        checked = bool(req.get("checked",False))

        # MySQLに問題を取得しにいく
        result = worst_quiz(file_num=file_num,category=category,image=image_flag,checked=checked)

        if(result['statusCode'] == 500):
            return {
                "statusCode" : 500,
                "error" : result["message"]
            }
        elif(len(result['result'])==0):
            return {
                "statusCode" : 404,
                "error" : "Not Found,指定された条件でのデータはありません(file_num:{0}, category:{1}, checked:{2})".format(file_num,category,checked)
            }
        else:
            # 取得結果を返す
            return {
                "statusCode" : 200,
                "response" : result['result'][0]
            }
    except Exception as e:
        return {
            "statusCode" : 500,
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
        if(result['statusCode'] == 500):
            return {
                "statusCode" : 500,
                "error" : result["message"]
            }
        else:
            return {
                "statusCode" : 200,
                "req" : req,
                "result" : result['result']
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
        "condition" : {
            "question": trueなら問題文を対象に検索
            "answer": trueなら答えを対象に検索
        }
        "category": カテゴリ
        "checked": チェック問題フラグ（オプション）
        "rate": 正解率以下指定（オプション）
    }

    Returns:
        result(JSON): 成功またはエラーログ
    """
    try:
        # リクエストから値を読み取る。
        req = request.json
        file_num = int(req.get("file_num"))
        query = req.get("query","")
        condition = req.get("condition","{}")
        category = req.get("category","")
        checked = bool(req.get("checked",False))
        rate = float(req.get("rate",100))
    
        # MySQLに問題を取得しにいく
        result = search_quiz(query,file_num,cond=condition,category=category,rate=rate,checked=checked)

        # 取得結果を返す
        if(result['statusCode'] == 500):
            return {
                "statusCode" : 500,
                "error" : result["message"]
            }
        elif(len(result['result'])==0):
            return {
                "statusCode" : 404,
                "error" : "Not Found,指定された条件でのデータはありません(file_num:{0}, query:{1}, category:{2}, checked:{3}, rate={4})".format(file_num,query,category,checked,rate)
            }
        else:
            return {
                "statusCode" : 200,
                "req" : req,
                "result" : result['result']
            }
    except Exception as e:
        return {
            "statusCode" : 500,
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
        "checked": チェック問題フラグ(オプション)
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
        checked = bool(req.get("checked",False))

        # MySQLに問題を取得しにいく
        result = minimum_quiz(file_num=file_num,category=category,image=image_flag,checked=checked)

        # 取得結果を返す
        if(result['statusCode'] == 500):
            return {
                "statusCode" : 500,
                "error" : result["message"]
            }
        elif(len(result['result'])==0):
            return {
                "statusCode" : 404,
                "error" : "Not Found,指定された条件でのデータはありません(file_num:{0}, category:{1}, checked:{2})".format(file_num,category,checked)
            }
        else:
            return {
                "statusCode" : 200,
                "response" : result['result'][0]
            }
    except Exception as e:
        return {
            "statusCode" : 500,
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

@app.route('/add', methods=["POST"])
def add():
    """問題追加API
    Args:  JSON
    {
        "file_num": ファイル番号,
        "data": 入力データ
    }

    Returns:
        [JSON] : 実行結果
    """
    try:
        # リクエストから値を読み取る。ない場合はデフォルト値
        req = request.json
        file_num = int(req.get("file_num",-1))
        data = req.get("data","")

        # INSERT処理実施
        result = add_quiz(file_num,data)

        # (JSON形式で)返す
        if(result['statusCode'] == 500):
            return {
                "statusCode" : 500,
                "error" : result["message"],
                "traceback" : result["traceback"]
            }
        else:
            return {
                "statusCode" : 200,
                "req" : req,
                "result" : result['result']
            }
    except Exception as e:
        return {
            'statusCode' : 500,
            "error" : traceback.format_exc()
        }

@app.route('/edit', methods=["POST"])
def edit():
    """問題追加API
    Args:  JSON
    {
        "file_num" (int): ファイル番号
        "quiz_num" (int): 問題番号
        "question" (str): 問題文
        "answer" (str): 答えの文
        "category" (str): カテゴリ
        "img_file" (str): 画像ファイル名
    }

    Returns:
        [JSON] : 実行結果
    """
    try:
        # リクエストから値を読み取る。ない場合はデフォルト値
        req = request.json
        file_num = int(req.get("file_num",-1))
        quiz_num = int(req.get("quiz_num",-1))
        question = req.get("question","")
        answer = req.get("answer","")
        category = req.get("category","")
        img_file = req.get("img_file","")

        # INSERT処理実施
        result = edit_quiz(file_num,quiz_num,question,answer,category,img_file)

        # (JSON形式で)返す
        if(result['statusCode'] == 500):
            return {
                "statusCode" : 500,
                "error" : result["message"],
                "traceback" : result["traceback"]
            }
        else:
            return {
                "statusCode" : 200,
                "req" : req,
                "result" : result['result']
            }
    except Exception as e:
        return {
            'statusCode' : 500,
            "error" : traceback.format_exc()
        }

@app.route('/get_category', methods=["POST"])
def category_list():
    try:
        # リクエストから値を読み取る。ない場合はデフォルト値
        req = request.json
        file_num = int(req.get("file_num",-1))

        # カテゴリ取得
        results = get_category(file_num)

        return {
            "statusCode" : 200,
            "result" : results['result']
        }

    except Exception as e:
        return {
            'statusCode' : 500,
            "error" : traceback.format_exc()
        }

@app.route('/edit_category_of_question', methods=["POST"])
def edit_category():
    try:
        # リクエストから値を読み取る。ない場合はデフォルト値
        req = request.json
        data = list(req.get("data",[]))

        # カテゴリ取得
        results = edit_category_of_question(data)

        return {
            "statusCode" : results['statusCode'],
            "result" : results['message']
        }

    except Exception as e:
        return {
            'statusCode' : 500,
            "error" : traceback.format_exc()
        }

@app.route('/update_category_master', methods=["GET"])
def ucm():
    try:
        # カテゴリマスタ更新関数を実行
        results = update_category_master()

        return {
            "statusCode" : results['statusCode'],
            "result" : results['message']
        }

    except Exception as e:
        return {
            'statusCode' : 500,
            "error" : traceback.format_exc()
        }

@app.route('/get_accuracy_rate_by_category', methods=["POST"])
def garbc():
    try:
        # リクエストから値を読み取る。ない場合はデフォルト値
        req = request.json
        file_num = int(req.get("file_num",-1))

        # カテゴリマスタ更新関数を実行
        results = get_accuracy_rate_by_category(file_num)

        return {
            "statusCode" : results['statusCode'],
            "result" : results['result']
        }

    except Exception as e:
        return {
            'statusCode' : 500,
            "error" : traceback.format_exc()
        }

@app.route('/edit_checked_of_question', methods=["POST"])
def edit_checked():
    try:
        # リクエストから値を読み取る。ない場合はデフォルト値
        req = request.json
        data = list(req.get("data",[]))

        # カテゴリ取得
        results = edit_checked_of_question(data)

        return {
            "statusCode" : results['statusCode'],
            "result" : results['message']
        }

    except Exception as e:
        return {
            'statusCode' : 500,
            "error" : traceback.format_exc()
        }

@app.route('/s3_file_download', methods=["POST"])
def img_download():
    """S3からファイルをダウンロードする関数
    Args:  JSON
    {
        "filename" (str): ファイル名
    }

    Returns:
        [type]: [description]
    """    
    try:
        # リクエストから値を読み取る。ない場合はデフォルト値
        req = request.json
        filename = str(req.get("filename",""))

        # ファイル取得
        result = file_download(filename)
        if(result['result']):
            # ファイルを取得できた場合
            return {
                "statusCode" : 200
            }
        else:
            # ファイルが取得できなかった場合
            return {
                "statusCode" : 400,
                "error" : result['error']
            }

    except Exception as e:
        return {
            'statusCode' : 500,
            "error" : traceback.format_exc()
        }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)