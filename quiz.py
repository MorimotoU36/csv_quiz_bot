import pandas as pd
import configparser
import sys
import random
import requests
import time

#設定ファイル読み込み
inifile="config/quiz.ini"
ini=""
try:
    ini = configparser.ConfigParser()
    ini.read(inifile, 'UTF-8')
except Exception as e:
    print("エラー：設定ファイル({0})が読み込めません".format(inifile))
    print(e)
    sys.exit()

#問題csv読み込み
df=""
quizfilename=""
try:
    quizfilename=ini['Filename']['QUIZFILE']
    df=pd.read_csv('csv/'+quizfilename)
except Exception as e:
    print("エラー：問題csv({0})の読み込み時にエラーが発生しました".format(quizfilename))
    print(e)
    sys.exit()

#全問題数
total=df.shape[0]
#ランダムに1個選ぶ
quiz_id=random.randrange(total)
#その問題を(リスト形式で)取ってくる
quiz=df.iloc[quiz_id,:].values.tolist()

quiz_num=quiz[0]
question=quiz[1]
answer=quiz[2]

#問題文作成
quiz_sentense="["+str(quiz_num)+"]:"+question

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
    print("エラー：問題メッセージ作成時にエラーが発生しました")
    print(e)
    sys.exit()
