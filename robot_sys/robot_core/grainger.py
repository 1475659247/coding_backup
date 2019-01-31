import requests
import traceback
from robot_core import ehsy
from config.config import *
from config.ua import *
from sql_orm.orm import *
from bs4 import BeautifulSoup
import os
import decimal

def update_site():
    parity_site = store_s.query(ParitySite).filter(ParitySite.site_id == GRAINGER_ID).first()
    if parity_site:
        parity_site.site_name = grainger_name
        parity_site.site_type = grainger_site_type
        parity_site.site_telephone = grainger_telephone
        parity_site.site_logo = grainger_logo_path
        parity_site.site_web = grainger_host
        parity_site.status = 0
    else:
        parity_site = ParitySite()
        parity_site.site_id = GRAINGER_ID
        parity_site.site_name = grainger_name
        parity_site.site_type = grainger_site_type
        parity_site.site_telephone = grainger_telephone
        parity_site.site_logo = grainger_logo_path
        parity_site.site_web = grainger_host
        parity_site.status = 0
        store_s.add(parity_site)
    store_s.commit()

def get_brand_logo(driver,url):
    brand_logo_url = ''
    try:
        html = http_get(url=url,driver=driver,mode=1,proxies=proxies)
        soup = BeautifulSoup(html, 'html.parser')
        main_soup = soup.find('div',attrs={"class":"brand-new-logo"})
        brand_logo_url = main_soup.find('img').get('src')
    except Exception as e:
        #print("error get_brand_logo:%s" % url)
        brand_logo_url = ''
    return brand_logo_url

def update_brand(driver,html):
    brand_id = 0
    soup = BeautifulSoup(html, 'html.parser')
    #update brand
    try:
        main_soup = soup.find('li',attrs={"id":"summary-brand"})
        brand_str = main_soup.find('a').text.lstrip().rstrip()
        brand_url = 'http://item.grainger.cn/' + main_soup.find('a').get('href')
        brand_zh_name = brand_str.split(' ')[0]
        uchar = brand_zh_name[0]
        uchar2 = brand_zh_name[-1]
        if (uchar < u'\u4e00' or uchar > u'\u9fa5') and (uchar2 < u'\u4e00' or uchar2 > u'\u9fa5'):
            brand_en_name = brand_zh_name
            brand_zh_name = ''
        else:
            for ft in grainger_str:
                brand_zh_name = brand_zh_name.split(ft)[0]
            try:
                brand_en_name = brand_str.split(' ')[1]
                uchar = brand_en_name[0]
                if ('\u0041' <= uchar<='\u005a') or ('\u0061' <= uchar<='\u007a') or ('0' <= uchar <= '9'):
                    brand_en_name = brand_en_name
                else:
                    brand_en_name = ''
            except:
                brand_en_name = ''
    except Exception as e:
        #print("Warning no brand: %s" % e)
        brand_zh_name = '国产'
        brand_en_name = ''

    if brand_zh_name == '无':
        brand_zh_name = '国产'
        brand_en_name = ''

    if brand_zh_name == '' and brand_en_name == '':
        return brand_id

    brand_search = ehsy.find_brand(brand_zh_name)
    brand_search_en = ehsy.find_brand(brand_en_name)
    if brand_search:
        brand_id = brand_search.brand_id
        if brand_search.brand_en_name == '':
            brand_search.brand_en_name = brand_en_name
        if brand_search.brand_logo == '':
            brand_logo_url = get_brand_logo(driver,brand_url)
            if brand_logo_url: 
                dir_path = 'brand'  + '/' + str(brand_search.brand_id) + '/'
                brand_search.brand_logo = dir_path + str(brand_search.brand_id) + '.' + brand_logo_url.split('.')[-1]
                brand_search.brand_logo_url = brand_logo_url
        store_s.commit()
    elif brand_search_en: 
        brand_id = brand_search_en.brand_id
        if brand_search_en.brand_zh_name == '':
            brand_search_en.brand_zh_name = brand_zh_name
        if brand_search_en.brand_logo == '':
            brand_logo_url = get_brand_logo(driver,brand_url)
            if brand_logo_url: 
                dir_path = 'brand'  + '/' + str(brand_search_en.brand_id) + '/'
                brand_search_en.brand_logo = dir_path + str(brand_search_en.brand_id) + '.' + brand_logo_url.split('.')[-1]
                brand_search_en.brand_logo_url = brand_logo_url
        store_s.commit()
    else:
        brand_search = store_s.query(ParityBrand).order_by(ParityBrand.brand_id.desc()).first()
        if brand_search:
            count = brand_search.brand_id
        else:
            count = 10000
        parity_brand = ParityBrand()
        parity_brand.brand_zh_name = brand_zh_name
        parity_brand.brand_en_name = brand_en_name
        brand_logo_url = get_brand_logo(driver,brand_url)
        parity_brand.brand_logo_url = brand_logo_url
        parity_brand.brand_id = count + 1
        brand_id = parity_brand.brand_id
        if brand_logo_url:
            dir_path = 'brand'  + '/' + str(parity_brand.brand_id) + '/'
            parity_brand.brand_logo = dir_path + str(parity_brand.brand_id) + '.' + parity_brand.brand_logo_url.split('.')[-1]
        else:
            parity_brand.brand_logo = ''
        store_s.add(parity_brand)
        store_s.commit()
    return brand_id

def parser_page(driver,url):
    try:
        count = 0
        html = http_get(url=url,driver=driver,mode=1,proxies=proxies)
        soup = BeautifulSoup(html, 'html.parser')
        try:
            main_soup = soup.find('div',attrs={"id":"name"})
            title = main_soup.text
            name = ''.join(title.split())
        except:
            print("Warning no name")
            raise Exception
        site_id = GRAINGER_ID
        brand_id = update_brand(driver,html)
        if brand_id == 0:
            return count
        try:
            main_soup = soup.find('a',attrs={"class":"jqzoom"})
            image_url = main_soup.find('img').get('src')
        except:
            print("Warning no image")
            image_url = ''
            
        main_soup = soup.find('table',attrs={"class":"productIndex"})
        sub_soup = main_soup.find('tbody')
        sub_soup_t = sub_soup.find_all('tr')
        for product in sub_soup_t:
            try:
                product_id = product.find('td',attrs={"class":"item_no"})
                product_id = product_id.find_all('a')[-1]
                product_url = 'http:' + product_id.get('href')
                product_id = product_id.get('href').split('/')[-2]
                product_id = 'GRAINGER' + "".join(product_id.split())
            except:
                print("Warning no product_id")
                raise Exception

            if image_url !='':
                dir_path = 'grainger/'
                image = dir_path + product_id + '.' + image_url.split('.')[-1]
            else:
                image = ''

            try:
                model = product.find('td',attrs={"class":"mfr_no"}).text
                model = "".join(model.split())
            except:
                print("Warning no model")
                model = ''
            
            try:
                price_soup = product.find('td',attrs={"class":"price"})
                price_1 = price_soup.text.split('￥')[-1].split('/')[0]
                price_2 = "".join(price_1.split())
                price = ("%.3f" % float(''.join(price_2.split(','))))
                price = decimal.Decimal(price)
            except Exception as e:
                #print("Warning no price:%s" % product_url)
                price = decimal.Decimal(0.000)
                continue

            try:
                goods_time_soup = product.find('td',attrs={"class":"group-shipping-time"})
                goods_time = goods_time_soup.text
                goods_time = ''.join(goods_time.split())
                goods_time = int(''.join(list(filter(str.isdigit,goods_time))))
            except:
                #print("Warning no goods_time ")
                goods_time = 0
            #
            sales = 0
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
                    parity_product.type = grainger_site_type
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
                    #print(parity_product)
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
                    parity_product.type = grainger_site_type
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
                time.sleep(random.random())
            except Exception as e:
                print("error commit:%s %s" % (e,parity_product))
                raise e
        return count
    except Exception as e:
        print("error parser_page:%s" % url)
        raise Exception

def parser_product_cgy(driver,url):
    try:
        count = 0
        html = http_get(url=url,driver=driver,mode=1,proxies=proxies)
        while True:
            soup = BeautifulSoup(html, 'html.parser')
            main_soup = soup.find_all('div',attrs={"class":"product_grid_box item"})
            if len(main_soup) == 0:
                re = test_ip('http://item.grainger.cn/s/c-2703/','劳保手套')
                if re == False:
                    print("error get product li")
                    raise Exception
                else:
                    print("ok product %s count:%d " % (url,count))
                    return count
            for product in main_soup:
                try:
                    product_url = "http://item.grainger.cn" + product.find('a').get('href')
                    count += parser_page(driver,product_url)
                except:
                    continue
            try:
                next_link = soup.find('a',text="下一页") 
                if next_link:
                    link = "http://item.grainger.cn/" + next_link.get('href')
                    html = http_get(url=link,driver=driver,mode=1,proxies=proxies)
                    print("next_page...")
                    continue
            except:
                print("error in parser_product_cgy next_page:%s " % e)
                raise e
            print("ok product %s count:%d " % (url,count))
            return count
    except Exception as e:
        print("error in parser_product_cgy:%s " % e)
        raise e

def crawler_product_info_cgy(goon=False):
    ipproxy = 2
    count = 0
    driver = open_driver(1)
    if goon == True:
        try:
            url = r.get("grainger_last_url")
            if url:
                r.rpush("grainger_category_url",url)
        except:
            print("error add last url:%s" % url)
    while True:
        try:
            url = r.rpop("grainger_category_url")
            if url == None:
                print("ok grainger_category_url empty")
                break
            r.set("grainger_last_url",url)
            url = str(url, encoding = "utf-8")
            print("begin crawler category:%s" % url)
            #url = "http://item.grainger.cn/s/c-2738/"
            count = parser_product_cgy(driver,url)
            #if count:
            #    break 
        except Exception as e: 
            re = test_ip('http://item.grainger.cn/s/c-2703/','劳保手套')
            if re == False:
                switch_ip()
            r.lpush("grainger_category_url",url)
            close_driver(driver,1)
            driver = open_driver(1)
            print("error in crawler_category_info:%s %s" % (url,e))
    close_driver(driver,1)

def crawler_category_url():
    ipproxy = 2
    r.delete("grainger_category_url")
    while True:
        try:
            driver = open_driver(1)
            html = http_get(url=grainger_host,driver=driver,mode=1,proxies=proxies)
            soup = BeautifulSoup(html, 'html.parser')
            menu_soup = soup.find('div',attrs={"class":"cate-list"})
            count = 0;
            if len(menu_soup) == 0:
                raise Exception
            sub_soup = menu_soup.find_all('div',attrs={"class":"cate-list-expand"})
            for sub in sub_soup:
                sub_t = sub.find_all('dd')
                for link_soup in sub_t:
                    try:
                        sub_soup_t = link_soup.find_all('a')
                        for link in sub_soup_t:
                            url = link.get('href')
                            print(url)
                            r.lpush("grainger_category_url",url)
                            count +=1
                    except Exception as e:
                        print("error in get_category failed %s" % link_soup)
                        continue
            if count != 0:
                print("ok category :count=%d"% count)
                close_driver(driver,1)
                break
        except Exception as e: 
            re = test_ip('http://item.grainger.cn/s/c-2703/','劳保手套')
            if re == False:
                switch_ip()
            close_driver(driver,1)
            print("error in retry crawler category %s" % e)

def test():
    re = test_ip('http://item.grainger.cn/s/c-2703/','劳保手套')
    if re == True:
        print("ip is ok")
    else:
        print("ip failed")
    '''

    url = "http://item.grainger.cn/g/00208897/"
    driver = open_driver(1)
    html = http_get(url=url,driver=driver,mode=1,proxies=proxies)
    soup = BeautifulSoup(html, 'html.parser')
    price_list = soup.find('table',attrs={"class":"productIndex"})
    #print(price_list)
    close_driver(driver,1)
    '''
