#!/bin/sh
date > ehsy.log
if [ $# == 0 ]
then
    echo "restart " >> ehsy.log
    nohup python -u ehsy_run.py 7 >> ehsy.log &
else
    if [ $1 == 'goon' ]
    then 
        echo "goon" >> ehsy.log
        nohup python -u ehsy_run.py 8 >> ehsy.log &
    else
        echo ":error:input ./ehsy_onekey.sh goon"
    fi
fi
