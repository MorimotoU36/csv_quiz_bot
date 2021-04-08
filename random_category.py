# -*- coding: utf-8 -*-
from argparse import ArgumentParser
import pandas as pd
import configparser
import sys
import random
import requests
import time
import os

#オプション読み取り
worstflag=False
if __name__ == '__main__':
    try:
        argparser = ArgumentParser()
        argparser.add_argument('-w', '--worst',
                           action='store_true',
                           help='一番正解率が悪いカテゴリを選ぶ')

        args = argparser.parse_args()
        worstflag=args.worst
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

#カテゴリリスト読み込み
cat_df=""
cat_name=""
quizfilename=""
try:
    quizfilename=ini['Filename']['QUIZFILE']
    cat_name='category_of_{0}_list.csv'.format(quizfilename[:-4])
    cat_df=pd.read_csv('category/'+cat_name)
except Exception as e:
    print("エラー：カテゴリリストが存在しません。category_accuracy_list.pyを実行して作成してください",file=sys.stderr)
    print(e,file=sys.stderr)
    os.chdir(pwd_dir)
    sys.exit()

#カテゴリを選ぶ
selected_cat=""
if(worstflag):
    #一番正解率が悪いカテゴリを選ぶ
    selected_cat=cat_df.sort_values('平均正解率[%]').iloc[0,:].values.tolist()[0]
else:
    #ランダムにカテゴリを1個選ぶ
    cat_total=cat_df.shape[0]
    cat_id=random.randrange(cat_total)
    selected_cat=cat_df.iloc[cat_id,:].values.tolist()[0]
print("カテゴリ：{0}".format(selected_cat))

#そのカテゴリの問題を取得する
df=""
try:
    df=pd.read_csv('csv/'+quizfilename)
    df=df.query('カテゴリ.str.contains("'+selected_cat+'")',engine='python')
except Exception as e:
    print("エラー：問題csv({0})の読み込み時にエラーが発生しました".format(quizfilename),file=sys.stderr)
    print(e,file=sys.stderr)
    os.chdir(pwd_dir)
    sys.exit()

#問題の出題順をランダムに決める
#iniファイルで設定している値かカテゴリに該当する問題数のうち少ない方の数だけ出す
total=df.shape[0]
id_lists=list(random.sample(list(range(total)),min(total,int(ini['Slack']['QUIZ_NUM_BY_CATEGORY']))))

for i in id_lists:

    #問題を(リスト形式で)取ってくる
    quiz=df.iloc[i,:].values.tolist()

    quiz_num=quiz[0]
    question=quiz[1]
    answer=quiz[2]
    correct_num=int(quiz[3])
    incorrect_num=int(quiz[4])

    #問題文作成
    accuracy="(正答率:{0:.2f}%)".format(100*correct_num/(correct_num+incorrect_num)) if (correct_num+incorrect_num)>0 else "(未回答)"
    quiz_sentense="["+str(quiz_num)+"]:"+question+accuracy

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