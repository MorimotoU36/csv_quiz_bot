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

#引数チェック
inputs=sys.argv
if(len(inputs) < 2):
    #引数の数が少ないとエラー
    print('エラー：引数の数が正しくありません ({0} 検索語句)'.format(inputs[0]),file=sys.stderr)
    sys.exit()

#オプション,検索語句設定、読み取り
i_flag=False
search_query=""
if __name__ == '__main__':
    try:
        argparser = ArgumentParser()
        argparser.add_argument('-i', '--ignorecase',
                            action='store_true',
                            help='半角英字の大文字小文字を無視')
        argparser.add_argument('query')

        args = argparser.parse_args()
        i_flag=args.ignorecase
        search_query=args.query
    except Exception as e:
        print("エラー：オプション引数の読み取りに失敗しました",file=sys.stderr)
        print(e,file=sys.stderr)
        sys.exit()

#カレントディレクトリからスクリプトのあるディレクトリへ移動
pwd_dir=os.getcwd()
pgm_dir=os.path.realpath(os.path.dirname(__file__))
os.chdir(pgm_dir)

#pandas文字幅設定
pd.set_option('display.unicode.east_asian_width', True)

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

#問題csv読み込み、検索語句を含む問題を取得する
df=""
quizfilename=""
try:
    quiz_file_ind=int(ini['Filename']['DEFAULT_QUIZ_FILE_NUM']) - 1
    quiz_file_names=json.loads(ini.get("Filename","QUIZ_FILE_NAME"))
    quizfilename=quiz_file_names[quiz_file_ind]
    df=pd.read_csv('csv/'+quizfilename["filename"])

    #問題文に検索語句を含む問題を抽出
    qst_df=df.query('テスト問題.str.contains("'+search_query+'",case='+ str(not i_flag) +')',engine='python')

    #表示する
    print("--- 問 ---")
    if(qst_df.shape[0]==0):
        print("検索語句「{0}」を問題文に含む問題はありません。".format(search_query))
    else:
        qst_df=qst_df.loc[:,['問題番号','テスト問題','正解']]
        print(qst_df.to_string(index=False))
    
    #答えに検索語句を含む問題を抽出
    ans_df=df.query('正解.str.contains("'+search_query+'",case='+ str(not i_flag) +')',engine='python')

    #表示する
    print("--- 答 ---")
    if(ans_df.shape[0]==0):
        print("検索語句「{0}」を答えに含む問題はありません。".format(search_query))
    else:
        ans_df=ans_df.loc[:,['問題番号','テスト問題','正解']]
        print(ans_df.to_string(index=False))


except Exception as e:
    print("エラー：問題csv({0})の読み込み時にエラーが発生しました".format(quizfilename),file=sys.stderr)
    print(e,file=sys.stderr)
    os.chdir(pwd_dir)
    sys.exit()

#元のディレクトリに戻る
os.chdir(pwd_dir)

