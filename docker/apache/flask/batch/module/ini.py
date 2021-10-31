# -*- coding: utf-8 -*-
import os
import configparser

def get_ini_parser():
    """
    設定ファイルを読み込んで返す。設定ファイルのパスは環境変数INIから読み込む
    Returns:
        configparser.Configparser(): 読み込んだ設定ファイルの内容
    """
    # 設定ファイル読み込み
    config = configparser.ConfigParser()
    config.read(os.environ['INI'])

    return config

