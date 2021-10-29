# -*- coding: utf-8 -*-
import configparser
import pandas as pd
import sys
import json
import os

def getQuestion(file_num,quiz_num):
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

    #問題csv読み込み
    df=""
    quizfilename=""
    csvname=""
    quiz_file_ind=-1
    try:
        quiz_file_names=json.loads(ini.get("Filename","QUIZ_FILE_NAME"))
        quiz_file_ind=file_num if (0 <= file_num and file_num < len(quiz_file_names)) else int(ini['Filename']['DEFAULT_QUIZ_FILE_NUM']) - 1
        quizfilename=quiz_file_names[quiz_file_ind]
        csvname=quizfilename['csvname']
        df=pd.read_csv('../csv/'+quizfilename['filename'])
        df["画像ファイル名"].fillna("",inplace=True)
    except Exception as e:
        print("エラー：問題csv({0})の読み込み時にエラーが発生しました".format(quizfilename))
        print(e,file=sys.stderr)
        os.chdir(pwd_dir)
        sys.exit()

    #全問題数
    total=df.shape[0]

    #入力した問題番号<全問題数　の場合はエラー終了
    if(quiz_num < 0 or quiz_num >= total):
        print('エラー：問題ファイル:{0}：問題番号を1~{1}の間で入力してください'.format(quizfilename,total),file=sys.stderr)
        os.chdir(pwd_dir)
        sys.exit()

    #その問題を(リスト形式で)取ってくる
    quiz=df.iloc[quiz_num,:].values.tolist()

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

    #返り値作成(JSON)
    res = {
        'sentense': quiz_sentense,
        'answer': quiz_answer
    }

    #元のディレクトリに戻る
    os.chdir(pwd_dir)

    return res