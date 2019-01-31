from config.config import *
from sql_orm.orm import *
from robot_core import digikey
from robot_core import vipmro
import multiprocessing
import time
import sys
def digikey_run(flag):
    if flag == 0:
        digikey.test()
    elif flag == 1:
        digikey.get_category()
    elif flag == 2:
        digikey.crawler_product_info(goon=True)
    elif flag == 3:
        digikey.update_site()
    elif flag == 6:
        digikey.update_site()
        digikey.get_category()
        digikey.crawler_product_info()
    return

if __name__ == "__main__":
    if len(sys.argv) <2:
        print("请指定任务代号,例如:python run.py 0\n ")
        exit() 
    flag = int(sys.argv[1])
    digikey_run(flag)
