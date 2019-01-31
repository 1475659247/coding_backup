#!/bin/sh
ps x|grep grainger_run.py |grep -v grep |awk '{print $1}'|xargs kill -9

