# -*- coding: utf-8 -*-
import pandas as pd
import configparser
import sys
import random
import requests
import time

#pandas文字幅設定
pd.set_option('display.unicode.east_asian_width', True)

#引数チェック
inputs=sys.argv
if(len(inputs) < 2):
    #引数の数が少ないとエラー
    print('エラー：引数の数が正しくありません ({0} 検索語句)'.format(inputs[0]),file=sys.stderr)
    sys.exit()

#検索語句読み取り
search_query=inputs[1]

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

#問題csv読み込み、検索語句を含む問題を取得する
df=""
quizfilename=""
try:
    quizfilename=ini['Filename']['QUIZFILE']
    df=pd.read_csv('csv/'+quizfilename)

    #問題文に検索語句を含む問題を抽出
    qst_df=df.query('テスト問題.str.contains("'+search_query+'")',engine='python')

    #表示する
    print("--- 問 ---")
    if(qst_df.shape[0]==0):
        print("検索語句「{0}」を問題文に含む問題はありません。".format(search_query))
    else:
        qst_df=qst_df.loc[:,['問題番号','テスト問題']]
        print(qst_df.to_string(index=False))
    
    #答えに検索語句を含む問題を抽出
    ans_df=df.query('正解.str.contains("'+search_query+'")',engine='python')

    #表示する
    print("--- 答 ---")
    if(ans_df.shape[0]==0):
        print("検索語句「{0}」を答えに含む問題はありません。".format(search_query))
    else:
        ans_df=ans_df.loc[:,['問題番号','テスト問題']]
        print(ans_df.to_string(index=False))


except Exception as e:
    print("エラー：問題csv({0})の読み込み時にエラーが発生しました".format(quizfilename))
    print(e)
    sys.exit()




