# -*- coding: utf-8 -*-
from argparse import ArgumentParser
import pandas as pd
import configparser
import sys
import random
import requests
import time
import json
import os

#オプション,数値読み取り
num=1
if __name__ == '__main__':
    try:
        argparser = ArgumentParser()
        argparser.add_argument('-n', '--number',type=int,
                                default=num,
                                help='出題する問題数')
        args = argparser.parse_args()

        num=int(args.number)
    except Exception as e:
        print("エラー：オプション引数の読み取りに失敗しました",file=sys.stderr)
        print(e,file=sys.stderr)
        sys.exit()

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
    print("エラー：設定ファイル({0})が読み込めません".format(inifile),file=sys.stderr)
    print(e,file=sys.stderr)
    os.chdir(pwd_dir)
    sys.exit()

#問題csv読み込み
df=""
quizfilename=""
try:
    quiz_file_ind=int(ini['Filename']['DEFAULT_QUIZ_FILE_NUM']) - 1
    quiz_file_names=json.loads(ini.get("Filename","QUIZ_FILE_NAME"))
    quizfilename=quiz_file_names[quiz_file_ind]
    df=pd.read_csv('csv/'+quizfilename)
except Exception as e:
    print("エラー：問題csv({0})の読み込み時にエラーが発生しました".format(quizfilename),file=sys.stderr)
    print(e,file=sys.stderr)
    os.chdir(pwd_dir)
    sys.exit()

#全問題数
total=df.shape[0]

#正解率計算（回答数0回の場合は0にする）
df['正解率']=df['正解数']/(df['正解数']+df['不正解数'])
df['正解率'].fillna(0,inplace=True)
#正解数、正解率でソート
quizlist=df.sort_values(['正解数','正解率'])

#１問出題する時は、正解率の悪い問題ワーストX問の中から一問を選ぶ
selected_id=0
if(num==1):
    #最小正解数の取得
    min_cor_num=int(df['正解数'].min())
    #その正解数の問題をランダムに選ぶ
    df=df.query('正解数=='+str(min_cor_num)) 
    selected_id=random.randint(0,df.shape[0]-1)

for i in range(num):
    #ソートした問題リストを１問ずつ出題する
    if(num != 1):
        selected_id=i
    quiz=quizlist.iloc[selected_id,:].values.tolist()

    quiz_num=quiz[0]
    question=quiz[1]
    answer=quiz[2]
    correct_num=int(quiz[3])
    incorrect_num=int(quiz[4])

    #問題文作成
    accuracy="(正答率:{0:.2f}%)".format(100*correct_num/(correct_num+incorrect_num)) if (correct_num+incorrect_num)>0 else "(未回答)"
    quiz_sentense="(最小正解数("+str(i+1)+")問題)["+str(quiz_num)+"]:"+question+accuracy

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
        os.chdir(pwd_dir)
        sys.exit()

#元のディレクトリに戻る
os.chdir(pwd_dir)