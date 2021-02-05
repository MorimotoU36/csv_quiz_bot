# -*- coding: utf-8 -*-
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
    #各問題の正解率算出
    df['正解率']=100*df['正解数']/(df['正解数']+df['不正解数'])
    df['正解率'].fillna(0,inplace=True)
except Exception as e:
    print("エラー：問題csv({0})の読み込み時にエラーが発生しました".format(quizfilename))
    print(e)
    sys.exit()


#カテゴリ抽出
categories=sorted(list(set(':'.join(df['カテゴリ'].values.tolist()).split(':'))))

#平均正解率算出
accuracy=[]
for c in categories:
    #カテゴリiを含むデータのみ抽出
    dfi=df.query('カテゴリ.str.contains("'+str(c)+'")',engine='python')
    #各問題の正解率の平均値を算出
    accuracy.append('{:.2f}%'.format(df['正解率'].mean()))

#データフレーム化
acc_df=pd.DataFrame([categories,accuracy])
acc_df=acc_df.T
acc_df=acc_df.rename(columns={0: 'カテゴリ',1: '平均正解率'})
print(acc_df)

