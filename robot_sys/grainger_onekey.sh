#!/bin/sh
date > grainger.log
if [ $# == 0 ]
then
    echo "restart " >> grainger.log
    nohup python -u grainger_run.py 3 >> grainger.log &
else
    if [ $1 == 'goon' ]
    then 
        echo "goon" >> grainger.log
        nohup python -u grainger_run.py 1 >> grainger.log &
    else
        echo ":error:input ./grainger_onekey.sh goon"
    fi
fi
