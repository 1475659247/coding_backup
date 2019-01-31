from config.config import *
from sql_orm.orm import *
from robot_core import ehsy
from robot_core import ehsy_product
import multiprocessing
import time
import sys
def ehsy_run(flag):
    if flag == 0:
        ehsy_product.test2()
    elif flag == 1:
        ehsy.update_brand()
    elif flag == 2:
        ehsy.get_category()
    elif flag == 3:
        count = 0
        cpus = multiprocessing.cpu_count()
        pool = multiprocessing.Pool()
        results = []
        count = ehsy.get_category()
        if count == 0:
            print("分类采集失败，请重新再试\n")
            return
        for i in range(0, cpus):
            result = pool.apply_async(ehsy_product.work,args=(i,))
            results.append(result)
        pool.close()
        pool.join()
    elif flag == 4:
        ehsy.update_site()
    elif flag == 5:
        count = 0
        count = ehsy.get_category()
        if count == 0:
            print("分类采集失败，请重新再试\n")
            return
        ehsy_product.work(0)
    elif flag == 6:
        ehsy.down_brand_img()
    elif flag == 7:
        count = 0
        print("update site...")
        ehsy.update_site()
        print("update brand...")
        ehsy.update_brand()
        print("update product...")
        count = ehsy.get_category()
        if count == 0:
            print("分类采集失败，请重新再试\n")
            return
        ehsy_product.work(0)
        print("update over")
    elif flag == 8:
        ehsy_product.work(p_id=0,goon=True)
        print("update over")
    return

if __name__ == "__main__":
    if len(sys.argv) <2:
        print("请指定任务代号,例如:python run.py 0\n \
               0: 测试环境 \n \
               1. 重新采集品牌 \n \
               2. 采集分类 \n \
               3. 多进程更新商品\n \
               4. 更新商户\n \
               5. 单进程更新商品\n \
               6. 下载商品图片 \n \
               8. 断点续爬")
        exit() 
    flag = int(sys.argv[1])
    ehsy_run(flag)
