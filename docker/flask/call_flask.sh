#!/bin/bash

PWD_DIR=${PWD}
APP_DIR=`dirname $0`

cd ${APP_DIR}
nohup python3 app.py &

cd ${PWD_DIR}
exit 0