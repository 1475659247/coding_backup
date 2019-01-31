#!/bin/sh
ps x|grep digikey_run.py |grep -v grep |awk '{print $1}'|xargs kill -9

