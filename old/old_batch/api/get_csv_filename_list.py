# -*- coding: utf-8 -*-
from argparse import ArgumentParser
import configparser
import sys
import json
import os

def getCsvFileNameList():
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

    #リストをJSONにして返す
    try:
        csv_name_list=[]
        file_names=json.loads(ini.get("Filename","QUIZ_FILE_NAME"))
        #JSONに変換
        res={'text': file_names}
        return res
    except Exception as e:
        print(e,file=sys.stderr)
        os.chdir(pwd_dir)
        sys.exit()

    #元のディレクトリに戻る
    os.chdir(pwd_dir)
