import pandas as pd
import configparser
import sys

#設定ファイル読み込み
inifile="config/quiz.ini"
quizfilename=""
try:
    ini = configparser.ConfigParser()
    ini.read(inifile, 'UTF-8')
    quizfilename=ini['Filename']['QUIZFILE']

except Exception as e:
    print("エラー：設定ファイル({0})が読み込めません".format(inifile))
    print(e)
    sys.exit()



print(quizfilename)
