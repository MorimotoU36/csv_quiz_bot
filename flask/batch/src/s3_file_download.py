# -*- coding: utf-8 -*-
import os
import sys
import boto3
import io
import traceback

sys.path.append(os.path.join(os.path.dirname(__file__), '../module'))
from ini import get_ini_parser

s3 = boto3.resource('s3')

def file_download(img_file_name):
    """S3からファイルをダウンロードするAPI

    Args:
        img_file_name (str): 取得するファイルの名前

    Returns:
        result (bool): ダウンロードが行えたかの結果
    """

    # 設定ファイルを呼び出してS3バケット名を取得
    ini = get_ini_parser()
    bucket = s3.Bucket(ini['AWS']['S3_BUCKET_NAME'])

    # ローカルの取得ファイル置き場を確認し、あるならそれを返す(True)
    img_file_path="../../img/" + img_file_name
    if(os.path.exists(img_file_path)):
        return True

    # ないならS3にファイルを取得しに行く
    try:
        # 取得したファイルをローカルのファイル置き場に置く
        bucket.download_file(img_file_name, img_file_path)

        # Trueを返す
        return True
    except Exception as e:
        # S3にない場合はFalseを返す
        print("Error! S3")
        print(traceback.format_exc())
        return False


if __name__=="__main__":
    file_download("img.jpg")