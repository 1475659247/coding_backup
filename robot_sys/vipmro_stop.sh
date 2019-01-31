#!/bin/sh
ps x|grep vipmro_run.py |grep -v grep |awk '{print $1}'|xargs kill -9
sleep 3
killall -9 phantomjs 

