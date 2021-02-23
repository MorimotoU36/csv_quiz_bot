# -*- coding: utf-8 -*-
from argparse import ArgumentParser
import pandas as pd
import configparser
import sys
import random
import requests
import time

#オプション設定
def get_option():
    argparser = ArgumentParser()
    argparser.add_argument('-s', '--sort',
                           action='store_true',
                           help='正解率順で昇順にソート')
    return argparser.parse_args()

sortflag=False
if __name__ == '__main__':
    args = get_option()
    sortflag=args.sort

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
    print("エラー：問題csv({0})の読み込み時にエラーが発生しました".format(quizfilename),file=sys.stderr)
    print(e,file=sys.stderr)
    sys.exit()


#カテゴリ抽出
categories=sorted(list(set(':'.join(df['カテゴリ'].values.tolist()).split(':'))))

#平均正解率算出
accuracy=[]
for c in categories:
    #カテゴリiを含むデータのみ抽出
    dfi=df.query('カテゴリ.str.contains("'+str(c)+'")',engine='python')
    #各問題の正解率の平均値を算出
    accuracy.append(dfi['正解率'].mean())

#データフレーム化、表示
acc_df=pd.DataFrame([categories,accuracy])
acc_df=acc_df.T
acc_df=acc_df.rename(columns={0: 'カテゴリ',1: '平均正解率[%]'})

#ソートオプションあったらソート
if(sortflag):
    acc_df=acc_df.sort_values('平均正解率[%]')
print(acc_df)

#カテゴリリストを保存
acc_df.to_csv('category/category_of_{0}_list.csv'.format(quizfilename[:-4]),index=False)