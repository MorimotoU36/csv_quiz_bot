# -*- coding: utf-8 -*-
import configparser
import json

ini = configparser.ConfigParser()
ini.read('/opt/python/quiz.ini', 'UTF-8')

def get_csv_name_list():
    quiz_file_names=json.loads(ini.get("Filename","QUIZ_FILE_NAME"))
    return [ qi["csvname"] for qi in quiz_file_names ]

def get_csv_file_name_list():
    quiz_file_names=json.loads(ini.get("Filename","QUIZ_FILE_NAME"))
    return [ qi["filename"] for qi in quiz_file_names ]
