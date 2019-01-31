#!/bin/sh
date > vipmro.log
nohup python -u vipmro_run.py 6 >> vipmro.log &
