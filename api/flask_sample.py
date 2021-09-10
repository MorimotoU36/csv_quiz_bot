from flask import Flask, redirect, request
from flask_cors import CORS 
import get_csv_filename_list
import get_question

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

app.run(port=8000, debug=True)
 