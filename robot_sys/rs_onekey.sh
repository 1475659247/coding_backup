#!/bin/sh
date > rs.log
if [ $# == 0 ]
then
    echo "restart " >> rs.log
    nohup python -u rs_run.py 3 >> rs.log &
else
    if [ $1 == 'goon' ]
    then 
        echo "goon" >> rs.log
        nohup python -u rs_run.py 2 >> rs.log &
    else
        echo ":error:input ./rs_onekey.sh goon"
    fi
fi
