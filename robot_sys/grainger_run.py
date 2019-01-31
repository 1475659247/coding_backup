from config.config import *
from sql_orm.orm import *
from robot_core import grainger
import multiprocessing
import time
import sys
def grainger_run(flag):
    if flag == 0:
        grainger.test()
    elif flag == 1:
        grainger.crawler_product_info_cgy(goon=True)
    elif flag == 2:
        grainger.crawler_category_url()
    elif flag == 3:
        grainger.update_site()
        grainger.crawler_category_url()
        grainger.crawler_product_info_cgy()
    return

if __name__ == "__main__":
    if len(sys.argv) <2:
        print("请指定任务代号,例如:python run.py 0\n ")
        exit() 
    flag = int(sys.argv[1])
    grainger_run(flag)
