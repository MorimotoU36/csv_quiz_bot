from flask import Flask, redirect, request
from flask_cors import CORS 
import get_csv_filename_list

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
    print(request.form["file"])
    return request.form["file"]

app.run(port=8000, debug=True)
 