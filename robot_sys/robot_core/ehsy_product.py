import requests
import traceback
import time
from config.config import *
from config.ua import *
from sql_orm.orm import *
from bs4 import BeautifulSoup
from robot_core.ehsy import *
import decimal
import multiprocessing
import os
def parser_product(driver,url):
    count = 0
    index_url = ehsy_host + '/'
    '''
    html = http_get(index_url,driver,0,5)
    if html == None:
        raise Exception
    '''
    while True:
        #html = http_get(url,driver,0,5)
        try:
            driver.get(url)
            time.sleep(2)
        except:
            pass
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        main_soup = soup.find('div',attrs={"id":"product-list"})
        sub_soup = main_soup.find_all('div',attrs={"class":"product"})
        if len(sub_soup) == 0:
            print("error page null:%s" % url)
            raise Exception

        for product in sub_soup:
            min_soup = product.find('ul',attrs={"class":"product-parameter"})
            product_list = min_soup.find_all('li')
            #
            try:
                product_id = 'EHSY' + product.get('data-text')
            except:
                print("failed no product_id :%s" % url)
                continue
            #
            try:
                model = product_list[1].text.strip()
            except:
                model = ''
            #
            site_id = EHSY_ID
            #
            try:
                brand_name = product_list[0].text.strip()
                brand_id = find_brand(brand_name).brand_id
            except:
                brand_id = 0
                #todo 要补充详情页的品牌抓取
                print("error no brand_id :%s %s" % (brand_name,url))
                continue
            #
            try:
                soup_t = product.find('span',attrs={"class":"now_money"})
                price = ("%.3f" % float(soup_t.get("title").strip()))
                price = decimal.Decimal(price)
            except:
                price = decimal.Decimal(0.000)
            #
            try:
                soup_t = product.find('span',attrs={"class":"stock"})
                goods_time = soup_t.text.strip().split('天')[0]
                goods_time = int(goods_time)
            except:
                goods_time = 0
            #
            try:
                soup_t = product.find('div',attrs={"class":"productName"})
                name = soup_t.find('a').get('title').strip()
                product_url = index_url + soup_t.find('a').get('href').split('/')[-1]
            except:
                name = ''
                product_url = ''
            #
            try:
                image_url = product.find('img').get('src')
            except:
                image_url = ''

            if image_url !='':
                dir_path = 'ehsy/'
                image = dir_path + product_id + '.' + image_url.split('.')[-1]
            else:
                image = ''

            try:
                parity_product = store_s.query(ParityProduct).filter(ParityProduct.product_id == product_id).first()
                if parity_product:
                    parity_product.model = model
                    parity_product.site_id = site_id
                    parity_product.brand_id = brand_id
                    parity_product.goods_time = goods_time
                    parity_product.name = name
                    parity_product.image_url = image_url
                    parity_product.image = image
                    parity_product.url = product_url
                    parity_product.type = 1
                    parity_product.status = 0
                    parity_product.sales = 0
                    parity_price = store_s.query(ParityPrice).filter(ParityPrice.id == parity_product.price_id).first()
                    if parity_price.price != price:
                        #print("old_parity:%s new_parity:%s" % (parity_price.price,price))
                        parity_price = ParityPrice()
                        parity_price.product_id = product_id
                        parity_price.price = price
                        parity_price.update_time = int(time.time())
                        store_s.add(parity_price)
                        store_s.flush()
                        #print("update price ok")
                        parity_product.price_id = parity_price.id
                        store_s.commit()
                    else:
                        parity_price.update_time = int(time.time())
                        store_s.commit()
                    print("ok update product:%s" % parity_product.product_id)
                else:
                    parity_product = ParityProduct()
                    parity_product.product_id = product_id
                    parity_product.model = model
                    parity_product.site_id = site_id
                    parity_product.brand_id = brand_id
                    parity_product.goods_time = goods_time
                    parity_product.name = name
                    parity_product.image_url = image_url
                    parity_product.image = image
                    parity_product.url = product_url
                    parity_product.type = 1
                    parity_product.status = 0
                    parity_product.sales = 0
                    parity_price = ParityPrice()
                    parity_price.product_id = product_id
                    parity_price.price = price
                    parity_price.update_time = int(time.time())
                    store_s.add(parity_price)
                    store_s.flush()
                    #print("add price ok")
                    parity_product.price_id = parity_price.id
                    store_s.add(parity_product)
                    store_s.commit()
                    print("ok add product:%s" % parity_product.product_id)
                #print(parity_product)
                count = count+1
            except Exception as e:
                print("error commit:%s %s" % (e,parity_product))
                break
        next_soup = soup.find('a',attrs={"class":"nexPage"})
        if next_soup:
            #print("next Page...\n")
            url = index_url + next_soup.get('href').split('/')[-1]
            continue
        else:
            print("ok product %s count:%d " % (url,count))
            break
            
def work(p_id,goon=False):
    ipproxy = 2
    driver = open_driver(0,ipproxy=ipproxy)
    if goon == True:
        try:
            url = r.get("ehsy_last_url")
            if url:
                r.rpush("ehsy_category_url",url)
        except:
            print("error add last url:%s" % url)

    while True:
        try:
            url = r.rpop("ehsy_category_url")
            if url == None:
                print("ok ehsy_category_url empty")
                break
            r.set("ehsy_last_url",url)
            url_ = str(url, encoding = "utf-8")
            print("begin crawler category:%s" % url)
            parser_product(driver,url_)
            if DEBUG_LEVEL != 0:
                break
        except Exception as e:
            re = test_ip('http://www.ehsy.com/category-2249','综合套装')
            if re == False:
                switch_ip()
            r.lpush("ehsy_category_url",url)
            close_driver(driver,0)
            driver = open_driver(0,ipproxy=ipproxy)
            print("failed product %s %s\n" % (e,url))
    close_driver(driver,0)

def work_t(p_id):
    while True:
        print('Run child process %s (%s)...' % (p_id, os.getpid()))
        time.sleep(2)

def test():
    url = "http://www.ehsy.com/category-17009"
    ipproxy = 2
    driver = open_driver(0,ipproxy=ipproxy)
    parser_product(driver,url)

def test2():
    url = r.lpop("ehsy_category_url")
    if url == None:
        print("ok ehsy_category_url empty")
    print('set ok %s' % url)
    '''
    url = r.get("ehsy_last_url")
    r.set("ehsy_last_url",url)
    print('set ok %s' % url)
    r.lpush("ehsy_category_url",url)
    '''

def run():
    for i in range(7):
        p = multiprocessing.Process(target=work)
        p.start()

if __name__ == '__main__':
    for i in range(7):
        p = multiprocessing.Process(target=work)
        p.start()
        #test()
