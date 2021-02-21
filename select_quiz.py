# -*- coding: utf-8 -*-
import pandas as pd
import configparser
import sys
import random
import requests
import time


#引数チェック
inputs=sys.argv
if(len(inputs) < 2):
    #引数の数が少ないとエラー
    print('エラー：引数の数が正しくありません ({0} 問題番号)'.format(inputs[0]),file=sys.stderr)
    sys.exit()

#問題番号読み取り
quiz_id=0
try:
    quiz_id=int(inputs[1])
    quiz_id-=1
except Exception as e:
    print('エラー：引数({0})を数字に変換できません'.format(inputs[1]),file=sys.stderr)
    print(e,file=sys.stderr)
    sys.exit()

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

#問題csv読み込み
df=""
quizfilename=""
try:
    quizfilename=ini['Filename']['QUIZFILE']
    df=pd.read_csv('csv/'+quizfilename)
except Exception as e:
    print("エラー：問題csv({0})の読み込み時にエラーが発生しました".format(quizfilename))
    print(e,file=sys.stderr)
    sys.exit()

#全問題数
total=df.shape[0]

#入力した問題番号<全問題数　の場合はエラー終了
if(quiz_id < 0 or quiz_id >= total):
    print('エラー：問題番号を1~{0}の間で入力してください'.format(total),file=sys.stderr)
    sys.exit()

#その問題を(リスト形式で)取ってくる
quiz=df.iloc[quiz_id,:].values.tolist()

quiz_num=quiz[0]
question=quiz[1]
answer=quiz[2]
correct_num=int(quiz[3])
incorrect_num=int(quiz[4])

#問題文作成
accuracy="(正答率:{0:.2f}%)".format(100*correct_num/(correct_num+incorrect_num)) if (correct_num+incorrect_num)>0 else "(未回答)"
quiz_sentense="["+str(quiz_num)+"]:"+question+accuracy

#答えの文作成
quiz_answer="["+str(quiz_num)+"]答:"+answer

try:
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
    sys.exit()
