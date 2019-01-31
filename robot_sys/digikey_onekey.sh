#!/bin/sh
date > digikey.log
if [ $# == 0 ]
then
    echo "restart " >> digikey.log
    nohup python -u digikey_run.py 6 >> digikey.log &
else
    if [ $1 == 'goon' ]
    then 
        echo "goon" >> digikey.log
        nohup python -u digikey_run.py 2 >> digikey.log &
    else
        echo ":error:input ./digikey_onekey.sh goon"
    fi
fi
