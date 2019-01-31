import requests
import traceback
from config.config import *
from config.ua import *
from robot_core import ehsy
from sql_orm.orm import *
from bs4 import BeautifulSoup
from lxml import etree
import os
import time
import decimal
import multiprocessing
from requests.utils import requote_uri

def get_logo_url(driver,url):
    brand_logo_url = ''
    return brand_logo_url
    '''
    cnt = 0
    while brand_logo_url == '':
        if cnt > 1:
            break
        try:
            #url = requote_uri(brand_url)
            html = http_get(url=url,driver=driver,mode=1,time_out=10)
            soup = BeautifulSoup(html, 'html.parser')
            main_soup = soup.find('td',attrs={"class":"supplier-logo"})
            sub_soup = main_soup.find('img')
            brand_logo_url = 'http:'+ sub_soup.get('src').split('?')[0]
            break
        except:
            cnt +=1
            brand_logo_url = ''
    return brand_logo_url
    '''

def update_brand(driver,brand_name,brand_url):
    brand_id = 0
    brand_zh_name = '' 
    brand_url_logo = ''
    brand_en_name = brand_name
    brand_search_en = ehsy.find_brand(brand_en_name)
    if brand_search_en: 
        brand_id = brand_search_en.brand_id
        if brand_search_en.brand_logo == '':
            brand_logo_url = get_logo_url(driver,brand_url)
            if brand_logo_url != '': 
                dir_path = 'brand'  + '/' + str(brand_search_en.brand_id) + '/'
                brand_search_en.brand_logo = dir_path + str(brand_search_en.brand_id) + '.' + brand_logo_url.split('.')[-1]
                brand_search_en.brand_logo_url = brand_logo_url
                store_s.commit()
        #print(brand_search_en)
    else:
        brand_logo_url = get_logo_url(driver,brand_url)
        brand_search = store_s.query(ParityBrand).order_by(ParityBrand.brand_id.desc()).first()
        if brand_search:
            count = brand_search.brand_id
        else:
            count = 10000
        parity_brand = ParityBrand()
        parity_brand.brand_zh_name = brand_zh_name
        parity_brand.brand_en_name = brand_en_name
        parity_brand.brand_logo_url = brand_logo_url
        parity_brand.brand_id = count + 1
        brand_id = parity_brand.brand_id
        if brand_logo_url !='':
            dir_path = 'brand'  + '/' + str(parity_brand.brand_id) + '/'
            parity_brand.brand_logo = dir_path + str(parity_brand.brand_id) + '.' + parity_brand.brand_logo_url.split('.')[-1]
        else:
            parity_brand.brand_logo = ''

        store_s.add(parity_brand)
        store_s.commit()
        #print(parity_brand)
    return brand_id

def get_category():
    while True:
        driver = open_driver(1)
        try:
            html = http_get(url=digikey_host,driver=driver,mode=1,time_out=10,proxies=proxies)
        except:
            pass
        try:
            count = 0;
            html = http_get(url=digikey_category,driver=driver,mode=1,time_out=10,proxies=proxies)
            soup = BeautifulSoup(html, 'html.parser')
            menu_soup = soup.find_all('a',attrs={"class":"catfilterlink"})
            if len(menu_soup):
                break
        except:
            re = test_ip('http://www.digikey.com.cn/zh/help/contact-us','通信中心')
            if re == False:
                switch_ip()
            close_driver(driver,0)
            print("retry get category")
            continue
        
    r.delete("digikey_category_url")
    for link_soup in menu_soup:
        try:
            url = digikey_host + link_soup.get('href')
            #print(url)
            r.lpush("digikey_category_url",url)
            count +=1
        except Exception as e:
            print("error get_category failed %s" % link_soup)
            continue
    print("ok category:%d" % count)
    close_driver(driver,1)

def parser_product(driver,url):
    category_url = url
    try:
        count = 0;
        while True:
            html = http_get(url=url,driver=driver,mode=1,time_out=10,proxies=proxies)
            time.sleep(random.random())
            selector = etree.HTML(html)
            price_xpath = selector.xpath('//tr[@class="tbloddrow"]/td[9]/a')
            brand_xpath = selector.xpath('//tr[@class="tbloddrow"]/td[12]/a')
            soup = BeautifulSoup(html, 'html.parser')
            menu_soup = soup.find_all('tr',attrs={"class":"tbloddrow"})
            price_xpath = selector.xpath('//tr[@class="tbloddrow"]/td[9]/a')
            brand_xpath = selector.xpath('//tr[@class="tbloddrow"]/td[12]/a')
            menu_soup2 = soup.find_all('tr',attrs={"class":"tblevenrow"})  
            price_xpath2 = selector.xpath('//tr[@class="tblevenrow"]/td[9]/a')
            brand_xpath2 = selector.xpath('//tr[@class="tblevenrow"]/td[12]/a')
            menu_soup += menu_soup2
            price_xpath += price_xpath2
            brand_xpath += brand_xpath2
            sub_soup = soup.find("div",attrs={"id":"brdFamilyNoLink"})
            category_name = sub_soup.text.strip()
            if len(menu_soup) == 0:
                print("error get product")
                raise Exception
            for index,product in enumerate(menu_soup):
                #
                try:
                    soup_t = product.find('a',attrs={"id":"manufacturerPartNumberLnk"})
                    model = soup_t.text.strip()
                    product_url = digikey_host + soup_t.get('href')
                    product_id = 'DIGIKEY' + product_url.split('recordId=')[-1]
                    name = category_name + ' ' + model
                except Exception as e: 
                    raise Exception
                #
                site_id = DIGIKEY_ID
                
                #
                cnt = 0
                try:
                    price = price_xpath[index].text.split('¥')[-1].replace('\n','').replace('\r','').strip()
                    if '电询' in price:
                        cnt = 4
                    price = ("%.3f" % float(''.join(price.split(','))))
                    price = decimal.Decimal(price)
                except:
                    price = decimal.Decimal(0.000)

                while price == decimal.Decimal(0.000):
                    price_url = digikey_host + price_xpath[index].get('href')
                    if cnt > 3:
                        print("Warning get price failed:%s" % price_url)
                        break
                    try:
                        html = http_get(url=price_url,driver=driver,mode=1,time_out=10,proxies=proxies)
                        soup_t = BeautifulSoup(html, 'html.parser')
                        main_soup_t = soup_t.select('''table[id="pricing"] > tr:nth-of-type(2) > td:nth-of-type(2)''')[0]
                        price = main_soup_t.text.split('¥')[-1].replace('\n','').replace('\r','').strip()
                        price = ("%.3f" % float(''.join(price.split(','))))
                        price = decimal.Decimal(price)
                        break
                    except:
                        cnt +=1
                        price = decimal.Decimal(0.000)
                #
                goods_time = 0
                '''
                try:
                    soup_t = product.find_all('td')
                    goods_time = soup_t[7].text.replace('\n','').replace('\r','').strip()
                    goods_time = int(''.join(list(filter(str.isdigit,goods_time))))
                except:
                    goods_time = 0
                '''
                #
                try:
                    brand_name = brand_xpath[index].text.replace('\n','').replace('\r','').strip()
                    brand_url = digikey_host + brand_xpath[index].get('href')
                    brand_id = update_brand(driver,brand_name,brand_url)
                except:
                    brand_id = 0
                # 
                sales = 0
                #
                try:
                    image_url = "http:" + product.find('img').get('src')
                except:
                    image_url = ''

                if image_url !='':
                    dir_path = 'digikey/'
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
                        parity_product.type = digikey_site_type
                        parity_product.status = 0
                        parity_product.sales = sales
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
                        parity_product.type = digikey_site_type
                        parity_product.status = 0
                        parity_product.sales = sales
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
                    raise e
                 
            next_page = soup.find('a',text="下一页") 
            if next_page:
                url = digikey_host + next_page.get("href")
                print("next_page...")
            else:
                print("ok %s product:%d" % (category_url,count))
                break
        return count
    except Exception as e:
        raise e

def crawler_product_info(goon=False):
    driver = open_driver(1)
    if goon == True:
        try:
            url = r.get("digikey_last_url")
            if url:
                r.rpush("digikey_category_url",url)
        except:
            print("error add last url:%s" % url)

    while True:
        try:
            category_url = r.rpop("digikey_category_url")
            if category_url == None:
                print("ok category_url empty")
                break
            r.set("digikey_last_url",category_url)
            category_url = str(category_url, encoding = "utf-8")
            print("begin crawler category:%s" % category_url)
            #category_url = "http://www.digikey.com.cn/search/zh/%E4%BC%A0%E6%84%9F%E5%99%A8-%E5%8F%98%E9%80%81%E5%99%A8/-/15030"
            url = requote_uri(category_url)
            count = parser_product(driver,url)
        except Exception as e:
            re = test_ip('http://www.digikey.com.cn/zh/help/contact-us','通信中心')
            if re == False:
                switch_ip()
            r.lpush("digikey_category_url",category_url)
            close_driver(driver,1)
            driver = open_driver(1)
            print("error crawler_product_info %s %s" % (url,e))
    close_driver(driver,1)

def update_site():
    parity_site = store_s.query(ParitySite).filter(ParitySite.site_id == DIGIKEY_ID).first()
    if parity_site:
        parity_site.site_name = digikey_name
        parity_site.site_type = digikey_site_type
        parity_site.site_telephone = digikey_telephone
        parity_site.site_logo = digikey_logo_path
        parity_site.site_web = digikey_host
        parity_site.status = 0
    else:
        parity_site = ParitySite()
        parity_site.site_id = DIGIKEY_ID
        parity_site.site_name = digikey_name
        parity_site.site_type = digikey_site_type
        parity_site.site_telephone = digikey_telephone
        parity_site.site_logo = digikey_logo_path
        parity_site.site_web = digikey_host
        parity_site.status = 0
        store_s.add(parity_site)
    store_s.commit()

def test():
    re = test_ip('http://www.digikey.com.cn/zh/help/contact-us','通信中心')
    if re == False:
        print("ip failed")
    else:
        print("ip ok")
