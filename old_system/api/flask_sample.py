# -*- coding: utf-8 -*-
from flask import Flask, redirect, request
from flask_cors import CORS 
import get_csv_filename_list
import get_question
import answer

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)
@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/getcsvlist')
def getCsvList():
    return str(get_csv_filename_list.getCsvFileNameList())

@app.route('/getquestion', methods=['GET', 'POST'])
def getQuestion():
    # 送信データを取得、バイト文字列なのでデコードする
    post_data=request.get_data().decode()
    file_num,quiz_num=post_data.split('-')
    print(file_num,quiz_num)
    print(get_question.getQuestion(int(file_num)-1,int(quiz_num)-1))
    return get_question.getQuestion(int(file_num)-1,int(quiz_num)-1)

@app.route('/correct', methods=['GET', 'POST'])
def correct():
    # 送信データを取得、バイト文字列なのでデコードする
    post_data=request.get_data().decode()
    file_num,quiz_num=post_data.split('-')
    print(file_num,quiz_num)
    return answer.correct(int(file_num)-1,int(quiz_num))

@app.route('/incorrect', methods=['GET', 'POST'])
def incorrect():
    # 送信データを取得、バイト文字列なのでデコードする
    post_data=request.get_data().decode()
    file_num,quiz_num=post_data.split('-')
    print(file_num,quiz_num)
    return answer.incorrect(int(file_num)-1,int(quiz_num))

app.run(host='0.0.0.0', port=80, debug=True)
