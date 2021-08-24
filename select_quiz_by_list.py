# -*- coding: utf-8 -*-
import pandas as pd
import configparser
import sys
import random
import requests
import time
import json
import os

#カレントディレクトリからスクリプトのあるディレクトリへ移動
pwd_dir=os.getcwd()
pgm_dir=os.path.realpath(os.path.dirname(__file__))
os.chdir(pgm_dir)

#設定ファイル読み込み
inifile="config/quiz.ini"
ini=""
try:
    ini = configparser.ConfigParser()
    ini.read(inifile, 'UTF-8')
except Exception as e:
    print("エラー：設定ファイル({0})が読み込めません".format(inifile))
    print(e,file=sys.stderr)
    sys.exit()

#問題csv、指定問題番号リスト読み込み
df=""
filename=""
try:
    quiz_file_ind=int(ini['Filename']['DEFAULT_QUIZ_FILE_NUM'])
    quiz_file_names=json.loads(ini.get("Filename","QUIZ_FILE_NAME"))
    filename=quiz_file_names[quiz_file_ind-1]
    df=pd.read_csv('csv/'+filename['filename'])

    filename=ini['Filename']['QUIZ_INDEX_LIST_NAME'] + '_' + filename['filename'][:-4] + '.dat'
    idx_df=pd.read_csv('config/'+filename)
except Exception as e:
    print("エラー：問題csv({0})の読み込み時にエラーが発生しました".format(filename),file=sys.stderr)
    print(e,file=sys.stderr)
    os.chdir(pwd_dir)
    sys.exit()

try:
    #指定問題番号からランダムに一つ取得
    total=idx_df.shape[0]
    quiz_id=int(idx_df.iloc[random.randint(0,total-1),0])-1

    #その問題を(リスト形式で)取ってくる
    quiz=df.iloc[quiz_id,:].values.tolist()

    quiz_num=quiz[0]
    question=quiz[1]
    answer=quiz[2]
    correct_num=int(quiz[3])
    incorrect_num=int(quiz[4])

    #問題文作成
    accuracy="(正答率:{0:.2f}%)".format(100*correct_num/(correct_num+incorrect_num)) if (correct_num+incorrect_num)>0 else "(未回答)"
    quiz_sentense="(復習リスト問題)["+str(quiz_num)+"]:"+question+accuracy

    #答えの文作成
    quiz_answer="["+str(quiz_num)+"]答:"+answer

    #設定値読み込み
    slackapi=ini['Slack']['SLACK_API_URL']
    slacktoken=ini['Slack']['SLACK_API_TOKEN']
    slackchannel=ini['Slack']['SLACK_CHANNEL']
    slackanschannel=ini['Slack']['SLACK_ANSWER_CHANNEL']
    thinkingtime=int(ini['Slack']['THINKING_TIME'])

    #Slack APIへPOSTするためのデータ作成
    data = {
        'token': slacktoken,
        'channel': slackchannel,
        'text': quiz_sentense
    }

    #Slack APIへPOSTする
    response = requests.post(slackapi, data=data)

    print("問題をPOSTしました:"+quiz_sentense)

    #指定秒スリープ
    time.sleep(thinkingtime)

    #Slack APIへ答えをPOSTするためのデータ作成
    data = {
        'token': slacktoken,
        'channel': slackanschannel,
        'text': quiz_answer
    }

    #Slack APIへ答えをPOSTする
    response = requests.post(slackapi, data=data)

    print("答えをPOSTしました:"+quiz_answer)


except Exception as e:
    print("エラー：問題メッセージ作成時にエラーが発生しました",file=sys.stderr)
    print(e,file=sys.stderr)
    os.chdir(pwd_dir)
    sys.exit()


#元のディレクトリに戻る
os.chdir(pwd_dir)