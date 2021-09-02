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


#カレントディレクトリからスクリプトのあるディレクトリへ移動
pwd_dir=os.getcwd()
pgm_dir=os.path.realpath(os.path.dirname(__file__))
os.chdir(pgm_dir)

#設定ファイル読み込み
inifile="../config/quiz.ini"
ini=""
try:
    ini = configparser.ConfigParser()
    ini.read(inifile, 'UTF-8')
except Exception as e:
    print("エラー：設定ファイル({0})が読み込めません".format(inifile))
    print(e,file=sys.stderr)
    os.chdir(pwd_dir)
    sys.exit()

#リストと番号取得して返す
try:
    csv_name_list=[]
    file_names=json.loads(ini.get("Filename","QUIZ_FILE_NAME"))
    for i,f in enumerate(file_names):
        csv_name_list.append([i+1,f['csvname']])

    print(csv_name_list)
except Exception as e:
    print(e,file=sys.stderr)
    os.chdir(pwd_dir)
    sys.exit()

#元のディレクトリに戻る
os.chdir(pwd_dir)
