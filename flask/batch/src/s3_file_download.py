# -*- coding: utf-8 -*-
import os
import sys
import boto3
import io
import traceback
import shutil

sys.path.append(os.path.join(os.path.dirname(__file__), '../module'))
from ini import get_ini_parser, get_messages_ini

def file_download(img_file_name):
    """S3からファイルをダウンロードするAPI

    Args:
        img_file_name (str): 取得するファイルの名前

    Returns:
        result (bool): ダウンロードが行えたかの結果
    """

    s3 = boto3.resource('s3')

    # 設定ファイルを呼び出してS3バケット名を取得
    messages = get_messages_ini()
    try:
        ini = get_ini_parser()
        bucket = s3.Bucket(ini['AWS']['S3_BUCKET_NAME'])
    except Exception as e:
        return {
            "result": False,
            "error" : messages['ERR_0007'],
            "traceback": traceback.format_exc()
        }

    # ローカルの取得ファイル置き場を確認し、あるならそれを返す(True)
    img_file_path = ini['AWS']['IMG_FILE_DIR'] + img_file_name
    if(os.path.exists(img_file_path)):
        return {
            "result": True
        }
    # ないならS3にファイルを取得しに行く
    try:
        # ファイルの一時置き場
        bucket.download_file(img_file_name, img_file_path)

        # 結果を返す
        if(os.path.exists(img_file_path)):
            return {
                "result": True
            }
        else:
            return {
                "result": False,
                "error" : messages['ERR_0008'].format(img_file_path),
                "traceback": traceback.format_exc()
            }
        
    except Exception as e:
        # S3にない場合はFalseを返す
        return {
            "result": False,
            "error" : messages['ERR_0009'].format(img_file_name),
            "traceback": traceback.format_exc()
        }


if __name__=="__main__":
    print('s3_file_download!!')