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


try:
    #設定値読み込み
    slackapi=ini['Slack']['SLACK_API_URL']
    slacktoken=ini['Slack']['SLACK_API_TOKEN']
    slackchannel=ini['Slack']['SLACK_CHANNEL']
    slackanschannel=ini['Slack']['SLACK_ANSWER_CHANNEL']
    thinkingtime=int(ini['Slack']['THINKING_TIME'])

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
                        "text": "正解！",
                        "type": "button",
                        "style":"primary",
                        "value": "1-1-1"
                    },
                    {
                        "name": "miss",
                        "text": "不正解..",
                        "type": "button",
                        "style":"danger",
                        "value": "1-1-0"
                    }
                ]
            }
        ]


    data = {
        "token": slacktoken,
        "channel": slackanschannel,
        "text": "ボタンテスト",
        "attachments": json.dumps(attachments)
    }

    #Slack APIへ答えをPOSTする
    requests.post(slackapi, data=data)

    print("ボタンをPOSTしました")

except Exception as e:
    print("エラー：問題メッセージ作成時にエラーが発生しました",file=sys.stderr)
    print(e,file=sys.stderr)
    os.chdir(pwd_dir)
    sys.exit()

#元のディレクトリに戻る
os.chdir(pwd_dir)

