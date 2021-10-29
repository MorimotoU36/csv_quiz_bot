import configparser
import requests
import json
import sys
import os

#カレントディレクトリからスクリプトのあるディレクトリへ移動
pwd_dir=os.getcwd()
pgm_dir=os.path.realpath(os.path.dirname(__file__))
os.chdir(pgm_dir)

#引数読み取り
inputs=sys.argv

# 全引数チェック解析（問題ファイル番号、問題番号、正解不正解の組み合わせになっているか確認）
answer_list=[]
if(len(inputs)%3 != 1):
    #引数の数が合ってない(スクリプト名 + (問題ファイル番号,問題番号,正解不正解)*x　の組み合わせで無い)とエラー
    print('エラー：引数の数が正しくありません ({0} [[問題ファイル番号,問題番号,正解(0)不正解(1)]...])'.format(inputs[0]),file=sys.stderr)
    os.chdir(pwd_dir)
    sys.exit()

for i in range(1,len(inputs),3):
    file_id=inputs[i]
    question_id=inputs[i+1]
    answer_data=inputs[i+2]
    if(answer_data != '0' and answer_data != '1'):
        #回答データが0,1以外だとエラー
        print('エラー：引数の問題番号{0}に対する解答データ{1}が正しくありません(0か1)'.format(question_id,answer_data),file=sys.stderr)
        os.chdir(pwd_dir)
        sys.exit()

    answer_list.append([file_id,question_id,answer_data])

#設定ファイル読み込み
inifile="config/quiz.ini"
ini=""
try:
    ini = configparser.ConfigParser()
    ini.read(inifile, 'UTF-8')
except Exception as e:
    print("エラー：設定ファイル({0})が読み込めません".format(inifile),file=sys.stderr)
    print(e,file=sys.stderr)
    os.chdir(pwd_dir)
    sys.exit()


# 解答データをAWS DynamoDBに一つずつ登録していく
url=ini['AWS']['ANSWER_REGISTER_API']
for ans_i in answer_list:

    #送信データ作成
    data = {
        'text': ans_i[0]+' '+ans_i[1]+' '+ans_i[2]
    }

    #AWS APIにデータ送信
    response = requests.post(url, data=data)

    #結果を表示
    print(response.text)
else:
    print('{0}個の解答データを登録しました'.format(len(answer_list)))

#元のディレクトリに戻る
os.chdir(pwd_dir)