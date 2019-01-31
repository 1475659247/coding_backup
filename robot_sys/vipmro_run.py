from config.config import *
from sql_orm.orm import *
from robot_core import vipmro
import multiprocessing
import time
import sys
def vipmro_run(flag):
    if flag == 0:
        vipmro.test()
    elif flag == 1:
        vipmro.crawler_brand_url()
    elif flag == 2:
        vipmro.crawler_product_info_cgy()
    elif flag == 3:
        vipmro.crawler_category_url()
        vipmro.crawler_product_info_cgy()
    elif flag == 5:
        vipmro.update_site()
    elif flag == 6:
        vipmro.update_site()
        vipmro.crawler_brand_url()
        vipmro.crawler_product_info()
        vipmro.crawler_category_url()
        vipmro.crawler_product_info_cgy()
    return

if __name__ == "__main__":
    if len(sys.argv) <2:
        print("请指定任务代号,例如:python run.py 0\n ")
        exit() 
    flag = int(sys.argv[1])
    vipmro_run(flag)
