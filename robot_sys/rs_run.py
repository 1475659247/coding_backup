from config.config import *
from sql_orm.orm import *
from robot_core import rs
import multiprocessing
import time
import sys
def rs_run(flag):
    if flag == 0:
        #rs.test()
        rs.update_site()
    elif flag == 1:
        rs.crawler_brand_url()
    elif flag == 2:
        rs.crawler_product_info(goon=True)
    elif flag == 3:
        rs.update_site()
        rs.crawler_brand_url()
        rs.crawler_product_info()
    return

if __name__ == "__main__":
    if len(sys.argv) <2:
        print("请指定任务代号,例如:python run.py 0\n ")
        exit() 
    flag = int(sys.argv[1])
    rs_run(flag)
