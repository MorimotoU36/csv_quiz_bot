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
csv_id=-1
num=1
allflag=False
if __name__ == '__main__':
    try:
        argparser = ArgumentParser()
        argparser.add_argument('-c','--csv',default=0,type=int,
                                help='出題する問題csvのID,0ならランダム')
        argparser.add_argument('-n', '--number',type=int,
                                default=num,
                                help='出題する問題数')
        argparser.add_argument('-a', '--all',action='store_true',
                                help='全ての問題集からランダムに出題する')
        args = argparser.parse_args()
        csv_id=int(args.csv)-1
        num=int(args.number)
        allflag=args.all
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
dfs=[]
quizfilename=""
try:
    quiz_file_ind=int(ini['Filename']['DEFAULT_QUIZ_FILE_NUM']) - 1
    quiz_file_names=json.loads(ini.get("Filename","QUIZ_FILE_NAME"))
    if(allflag or csv_id != -1):
        for i in range(len(quiz_file_names)):
            quizfilename=quiz_file_names[i]["filename"]
            dfs.append(pd.read_csv('csv/'+quizfilename))
    else:
        quizfilename=quiz_file_names[quiz_file_ind]["filename"]
        df=pd.read_csv('csv/'+quizfilename)
except Exception as e:
    print("エラー：問題csv({0})の読み込み時にエラーが発生しました".format(quizfilename),file=sys.stderr)
    print(e,file=sys.stderr)
    os.chdir(pwd_dir)
    sys.exit()

#入力値(csv_id)チェック
if(csv_id!=-1 and (csv_id <0 or len(dfs)<=csv_id)):
    print("エラー：問題csv番号({0})は0(ランダム)または{1}~{2}の間で入力してください".format(csv_id+1,1,len(dfs)),file=sys.stderr)
    os.chdir(pwd_dir)
    sys.exit()

#正解率計算（回答数0回の場合は0にする）
for dfi in dfs:
    dfi['正解率']=dfi['正解数']/(dfi['正解数']+dfi['不正解数'])
    dfi['正解率'].fillna(0,inplace=True)
    #正解率、不正解数でソート
    dfi.sort_values(['正解率','不正解数'],inplace=True)

for i in range(num):
    #-a指定の時は問題集をランダムに選択,csv_idがある時はその問題集を選択
    file_ind=-1
    if(csv_id!=-1):
        df=dfs[csv_id]
    elif(allflag):
        df=random.choice(dfs)

    #全問題数
    total=df.shape[0]

    #ソートした問題リストをワーストn問目の問題を出題する
    quiz=df.iloc[i,:].values.tolist()

    quiz_num=quiz[0]
    question=quiz[1]
    answer=quiz[2]
    correct_num=int(quiz[3])
    incorrect_num=int(quiz[4])

    #問題文作成
    accuracy="(正答率:{0:.2f}%)".format(100*correct_num/(correct_num+incorrect_num)) if (correct_num+incorrect_num)>0 else "(未回答)"
    quiz_sentense="(worst("+str(i+1)+")問題)["+str(quiz_num)+"]:"+question+accuracy

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