from flask import Flask, redirect
import get_csv_filename_list

app = Flask(__name__, static_folder='.', static_url_path='')
@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/getcsvlist')
def getCsvList():
    return str(get_csv_filename_list.getCsvFileNameList())

app.run(port=8000, debug=True)
 