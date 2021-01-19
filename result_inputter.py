import configparser
import requests
import pandas as pd
import json
import sys

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

#AWS APIにアクセスして結果取得
response = requests.post(ini['AWS']['RESULT_GET_API'])

#json形式にパース
results=json.loads(response.text)
results=results['text']

#空なら終了
if(results == []):
    print("データ0件です")
    sys.exit()

#問題csv読み込み
df=""
quizfilename=""
try:
    quizfilename=ini['Filename']['QUIZFILE']
    df=pd.read_csv('csv/'+quizfilename)
except Exception as e:
    print("エラー：問題csv({0})の読み込み時にエラーが発生しました".format(quizfilename))
    print(e)
    sys.exit()

#結果データを解析
try:
    for r in results:
        quiz_id=r['quiz_id']
        ans=r['result']
        
        #quiz_idが何行目にあるかを調べる
        index=df.loc[df['問題番号'] == quiz_id].index[0]

        if(ans != "0"):
            #正解
            df.at[index,'正解数'] = str(int(df.at[index,'正解数']) + 1)
        else:
            #不正解
            df.at[index,'不正解数'] = str(int(df.at[index,'不正解数']) + 1)
        
        print("問題["+quiz_id+"]:"+("正解" if ans != "0" else "不正解")+"+1")
    
    #反映した結果をcsvに更新する
    df.to_csv('csv/'+quizfilename,index=False)
except Exception as e:
    print("エラー：csv({0})への正解データ登録時にエラーが発生しました".format(quizfilename))
    print(e)
    sys.exit()

