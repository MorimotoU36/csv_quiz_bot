#!/bin/bash

PWD_DIR=${PWD}
APP_DIR=`dirname $0`

cd ${APP_DIR}

# 全テスト実行
python3 -m unittest discover .

cd ${PWD_DIR}
exit 0