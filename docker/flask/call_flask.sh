#!/bin/bash

PWD_DIR=${PWD}
APP_DIR=`dirname $0`

cd ${APP_DIR}
echo "-----------------------------" >> nohup.out
echo `date "+%Y/%m/%d %H:%M:%S"` >> nohup.out
nohup python3 app.py &

cd ${PWD_DIR}
exit 0