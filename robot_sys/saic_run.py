from config.config import *
from sql_orm.orm import *
from robot_core import saic
import multiprocessing
import time
import sys
def rs_run(flag):
    if flag == 0:
        saic.test()
    return

if __name__ == "__main__":
    if len(sys.argv) <2:
        print("请指定任务代号,例如:python run.py 0\n ")
        exit() 
    flag = int(sys.argv[1])
    rs_run(flag)
