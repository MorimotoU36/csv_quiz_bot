import configparser
import requests
import shutil
import pandas as pd
import json
import sys
import os

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

#AWS APIにアクセスして結果取得
response = requests.post(ini['AWS']['RESULT_GET_API'])

#json形式にパース
results=json.loads(response.text)
results=results['text']

#空なら終了
if(results == []):
    print("データ0件です")
    sys.exit()

#問題csvのバックアップファイル作成
quiz_file_names=[]
try:
    quiz_file_names=json.loads(ini.get("Filename","QUIZ_FILE_NAME"))
    for i in range(len(quiz_file_names)):
        quizfilename=quiz_file_names[i]
        shutil.copyfile('csv/'+quizfilename,'csv/bkup/'+quizfilename+'.bkup')
except Exception as e:
    print("エラー：問題csv({0})のバックアップファイル作成時にエラーが発生しました".format(quizfilename),file=sys.stderr)
    print(e,file=sys.stderr)
    os.chdir(pwd_dir)
    sys.exit()

#DBからの解答データのバックアップファイル作成
try:
    db_df=pd.DataFrame(results)
    db_df.to_csv('csv/bkup/DB_bkup.csv',index=False)
except Exception as e:
    print("エラー：問題csv({0})のバックアップファイル作成時にエラーが発生しました".format(quizfilename),file=sys.stderr)
    print(e,file=sys.stderr)
    os.chdir(pwd_dir)
    sys.exit()


#問題csv読み込み
df=[]
try:
    for i in range(len(quiz_file_names)):
        df.append(pd.read_csv('csv/'+quiz_file_names[i]))
except Exception as e:
    print("エラー：問題csv({0})の読み込み時にエラーが発生しました".format(quizfilename),file=sys.stderr)
    print(e,file=sys.stderr)
    os.chdir(pwd_dir)
    sys.exit()

#結果データを解析
try:
    for r in results:
        file_id=r['file_id']
        quiz_id=r['quiz_id']
        ans=r['result']

        #エラーハンドリング：ファイル番号・問題番号が数字であるか？または有効な範囲内の数字であるかを確認
        if(not file_id.isdecimal() or int(file_id) <= 0 or len(quiz_file_names) < int(file_id) ):
            print('エラー：問題ファイル番号[{0}]はありません、飛ばします'.format(file_id),file=sys.stderr)
            continue
        elif(not quiz_id.isdecimal() or int(quiz_id) <= 0 or df[int(file_id)-1].shape[0] < int(quiz_id) ):
            print('エラー：問題番号[{0}]はありません、飛ばします'.format(quiz_id),file=sys.stderr)
            continue
        
        #指定したfile_idのdfを取り出す
        df_i=df[int(file_id)-1]

        #df_iを問題番号でソート
        df_i.sort_values('問題番号',inplace=True)
        #quiz_idが何行目にあるかを調べる
        idx=df_i.loc[df_i['問題番号'] == int(quiz_id)].index[0]

        if(ans != "0"):
            #正解
            df_i.at[idx,'正解数'] = str(int(df_i.at[idx,'正解数']) + 1)
        else:
            #不正解
            df_i.at[idx,'不正解数'] = str(int(df_i.at[idx,'不正解数']) + 1)
        
        #df_iを反映する
        df[int(file_id)-1]=df_i

        print("問題ファイル["+quiz_file_names[int(file_id)-1]+"] 問題["+quiz_id+"]:"+("正解" if ans != "0" else "不正解")+"+1")
    
    #反映した結果をcsvに更新する
    for i in range(len(quiz_file_names)):
        df[i].to_csv('csv/'+quiz_file_names[i],index=False)

    print('{0}個の解答データを登録しました'.format(len(results)))
except Exception as e:
    print("エラー：csv({0})への正解データ登録時にエラーが発生しました".format(quizfilename),file=sys.stderr)
    print(e,file=sys.stderr)
    os.chdir(pwd_dir)
    sys.exit()

#元のディレクトリに戻る
os.chdir(pwd_dir)