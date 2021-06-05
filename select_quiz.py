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
import boto3

#オプション,数値読み取り
csv_id=-1
quiz_id=-1
isDisplayImage=False
if __name__ == '__main__':
    try:
        argparser = ArgumentParser()
        argparser.add_argument('-c','--csv',default=-1,type=int,
                                help='出題する問題csvのID')
        argparser.add_argument('quiz_id',type=int,
                                help='出題する問題番号')
        argparser.add_argument('-i','--image',action='store_true',
                                help='登録画像を出力する場合指定')
        args = argparser.parse_args()
        csv_id=int(args.csv)-1
        quiz_id=int(args.quiz_id)-1
        isDisplayImage=args.image
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
    print("エラー：設定ファイル({0})が読み込めません".format(inifile))
    print(e,file=sys.stderr)
    os.chdir(pwd_dir)
    sys.exit()

#問題csv読み込み
df=""
quizfilename=""
csvname=""
quiz_file_ind=-1
try:
    quiz_file_names=json.loads(ini.get("Filename","QUIZ_FILE_NAME"))
    quiz_file_ind=csv_id if (0 <= csv_id and csv_id < len(quiz_file_names)) else int(ini['Filename']['DEFAULT_QUIZ_FILE_NUM']) - 1
    quizfilename=quiz_file_names[quiz_file_ind]
    csvname=quizfilename['csvname']
    df=pd.read_csv('csv/'+quizfilename['filename'])
    df["画像ファイル名"].fillna("",inplace=True)
except Exception as e:
    print("エラー：問題csv({0})の読み込み時にエラーが発生しました".format(quizfilename))
    print(e,file=sys.stderr)
    os.chdir(pwd_dir)
    sys.exit()

#全問題数
total=df.shape[0]

#入力した問題番号<全問題数　の場合はエラー終了
if(quiz_id < 0 or quiz_id >= total):
    print('エラー：問題ファイル:{0}：問題番号を1~{1}の間で入力してください'.format(quizfilename,total),file=sys.stderr)
    os.chdir(pwd_dir)
    sys.exit()

#その問題を(リスト形式で)取ってくる
quiz=df.iloc[quiz_id,:].values.tolist()

quiz_num=quiz[0]
question=quiz[1]
answer=quiz[2]
correct_num=int(quiz[3])
incorrect_num=int(quiz[4])
image_url=str(quiz[6])

#問題文作成
accuracy="(正答率:{0:.2f}%)".format(100*correct_num/(correct_num+incorrect_num)) if (correct_num+incorrect_num)>0 else "(未回答)"
quiz_sentense="["+csvname+"-"+str(quiz_num)+"]:"+question+accuracy

#答えの文作成
quiz_answer="["+csvname+"-"+str(quiz_num)+"]答:"+answer

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
    attachments=[
        {
            "text": "この問題に..",
            "title": "解答ボタン",
            "callback_id": "callback_id value",
            "color": "#FFFFFF",
            "attachment_type": "default",
            "actions": [
                {
                    "name": "clear",
                    "text": "正解した！",
                    "type": "button",
                    "style":"primary",
                    "value": str(quiz_file_ind+1)+"-"+str(quiz_num)+"-1"
                },
                {
                    "name": "miss",
                    "text": "不正解..",
                    "type": "button",
                    "style":"danger",
                    "value": str(quiz_file_ind+1)+"-"+str(quiz_num)+"-0"
                }
            ]
        }
    ]
    
    data = {
        'token': slacktoken,
        'channel': slackanschannel,
        'text': quiz_answer,
        "attachments": json.dumps(attachments)
    }

    #Slack APIへ答えをPOSTする
    requests.post(slackapi, data=data)

    print("答えをPOSTしました:"+quiz_answer)

    if(isDisplayImage):
        if(image_url == ""):
            print("警告:問題番号[{0}]の画像ファイルはありません".format(quiz_num))
        else:
            #画像ダウンロード
            s3 = boto3.resource('s3')
            bucket = s3.Bucket(ini['AWS']['S3_BUCKET_NAME'])
            bucket.download_file(image_url, image_url)

            #画像POST
            files = {'file': open(image_url, 'rb')}
            data = {
                'token': slacktoken,
                'channels': slackanschannel,
                'filename':image_url,
                'initial_comment': "",
                'title': image_url
            }
            requests.post(url=ini['Slack']['SLACK_FILE_UPLOAD_URL'], params=data, files=files)

            #画像削除
            os.remove(image_url)

except Exception as e:
    print("エラー：問題メッセージ作成時にエラーが発生しました",file=sys.stderr)
    print(e,file=sys.stderr)
    os.chdir(pwd_dir)
    sys.exit()

#元のディレクトリに戻る
os.chdir(pwd_dir)
