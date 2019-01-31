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
    parity_site = store_s.query(ParitySite).filter(ParitySite.site_id == RS_ID).first()
    if parity_site:
        parity_site.site_name = rs_name
        parity_site.site_type = rs_site_type
        parity_site.site_telephone = rs_telephone
        parity_site.site_logo = rs_logo_path
        parity_site.site_web = rs_host
        parity_site.status = 0
    else:
        parity_site = ParitySite()
        parity_site.site_id = RS_ID
        parity_site.site_name = rs_name
        parity_site.site_type = rs_site_type
        parity_site.site_telephone = rs_telephone
        parity_site.site_logo = rs_logo_path
        parity_site.site_web = rs_host
        parity_site.status = 0
        store_s.add(parity_site)
    store_s.commit()

def crawler_brand_url():
    rs_brand = 'http://china.rs-online.com/web/ob/%E6%88%91%E4%BB%AC%E7%9A%84%E5%93%81%E7%89%8C/'
    while True:
        try:
            r.delete("rs_brand_url")
            driver = open_driver(1)
            html = http_get(url=rs_brand,driver=driver,mode=1,proxies=proxies)
            soup = BeautifulSoup(html, 'html.parser')
            menu_soup = soup.find('table',attrs={"class":"allBrandsNavigationTbl"})
            brand_category = menu_soup.find_all('a')
            count = 0;
            if len(brand_category) == 0:
                raise Exception
            for brands in brand_category:
                brand_category_url  = brands.get('href')
                html = http_get(url=brand_category_url,driver=driver,mode=1,proxies=proxies)
                soup = BeautifulSoup(html, 'html.parser')
                menu_soup = soup.find('table',attrs={"class":"allBrandsTbl"})
                brand_list = menu_soup.find_all('a')
                for brand in brand_list:
                    brand_url = brand.get('href')
                    #print(brand_url)
                    r.lpush("rs_brand_url",brand_url)
                    count +=1
            if count != 0:
                print("ok category :count=%d"% count)
                close_driver(driver,1)
                break
        except Exception as e: 
            re = test_ip('http://china.rs-online.com/web/b/abus/','ABUS')
            if re == False:
                switch_ip()
            close_driver(driver,1)
            print("error in retry crawler category %s" % e)

def update_brand(brand_name,brand_logo_url=''):
    #update brand
    brand_id = 0
    brand_zh_name = ''
    brand_en_name = brand_name
    if brand_zh_name == '' and brand_en_name == '':
        return brand_id

    brand_search_en = ehsy.find_brand(brand_en_name)
    if brand_search_en: 
        brand_id = brand_search_en.brand_id
        if brand_search_en.brand_logo == '':
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

def parser_product_webdriver(url):
    try:
        ipproxy = 2
        driver = open_driver(0,ipproxy=ipproxy)
        count = 0
        html = ''
        try:
            driver.get(url)
            time.sleep(2)
        except:
            pass
        html = driver.page_source
        last_product = None
        while True:
            soup = BeautifulSoup(html, 'html.parser')
            main_soup = soup.find('table',attrs={"class":"srtnListTbl"})
            sub_soup = main_soup.find_all('tr',attrs={"class":"resultRow"})
            if last_product in sub_soup:
                print("Warning hit same...")
                switch_ip()
                raise Exception
            else:
                last_product = sub_soup[-1]
            if len(sub_soup) == 0:
                print("error get product li")
                raise Exception
            for product in sub_soup:
                try:
                    soup_t = product.find('a',attrs={"class":"tnProdDesc"})
                    name = soup_t.text.strip()
                    product_url = soup_t.get("href")
                    product_id = 'RS' + product_url.split('/')[-2]
                except Exception as e: 
                    raise Exception
                #
                try:
                    soup_0 = product.find('div',attrs={"class":"partColContent"})
                    soup_t = soup_0.find('ul',attrs={"class":"viewDescList"})
                    soup_tt = soup_t.find_all('li')[1]
                    brand_name = soup_tt.find('a').text.strip()
                    brand_id = update_brand(brand_name)
                    if brand_id == 0:
                        continue
                except Exception as e: 
                    continue

                #
                try:
                    soup_0 = product.find('div',attrs={"class":"partColContent"})
                    soup_t = soup_0.find('ul',attrs={"class":"viewDescList"})
                    soup_tt = soup_t.find_all('li')[2]
                    model = soup_tt.find_all('span')[-1].text.strip()
                except:
                    model = ''
                #
                site_id = RS_ID
                #
                try:
                    soup_0 = product.find('div',attrs={"class":"priceFixedCol"})
                    soup_t = soup_0.find('ul',attrs={"class":"viewDescList"})
                    soup_tt = soup_t.find_all('li')[1]
                    soup_ttt = soup_tt.find_all('span')[0]
                    price = soup_ttt.text.split('RMB')[-1].replace('\n','').replace('\r','').strip()
                    price = ("%.3f" % float(''.join(price.split(','))))
                    price = decimal.Decimal(price)
                except:
                    price = decimal.Decimal(0.000)

                #
                goods_time = 0

                #
                sales = 0
                #
                try:
                    image_url = 'http:' + product.find('img').get('src')
                except:
                    image_url = ''
                   
                if image_url !='':
                    dir_path = 'rs/'
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
                        parity_product.type = rs_site_type
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
                        parity_product.type = rs_site_type
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
            soup_t = soup.find('a',attrs={"title":"下一页"})
            if soup_t:
                try:
                    option = driver.find_element_by_xpath("//div[@class='checkoutPaginationContent']/a[@title='下一页']")
                    option.click()
                    time.sleep(3)
                    html = driver.page_source
                    #print("next_page...")
                    continue
                except Exception as e:
                    print("error next page:%s %s" % (e,url))
                    raise e
             
            print("ok product %s count:%d " % (url,count))
            close_driver(driver,0)
            return count
    except Exception as e:
        close_driver(driver,0)
        print("error in parser_product_webdriver:%s " % e)
        raise e

def parser_product_cgy(driver,url):
    try:
        count = 0
        html = http_get(url=url,driver=driver,mode=1,proxies=proxies)
        soup = BeautifulSoup(html, 'html.parser')
        main_soup = soup.find('img',attrs={"class":"brandLogoImg"})
        if main_soup:
            brand_name = main_soup.get('title')
            brand_logo_url = 'http:' + main_soup.get('src')
            update_brand(brand_name,brand_logo_url)
        main_soup = soup.find('div',attrs={"class":"brandFullCatContainer"})
        if main_soup:
            brand_list = main_soup.find_all('a',attrs={"class":"catLink"})
            for brand in brand_list:
                brand_url = brand.get('href')
                #print(brand_url)
                r.lpush("rs_brand_url",brand_url)
            return count
        main_soup = soup.find('div',attrs={"class":"srtnLeftDiv brandPage"})
        if main_soup:
            brand_list = main_soup.find_all('div',attrs={"class":"categoryLink"})
            for brand in brand_list:
                brand_url = brand.find('a').get('href')
                #print(brand_url)
                r.lpush("rs_brand_url",brand_url)
            return count
        count = parser_product_webdriver(url) 
    except Exception as e:
        print("error in parser_product_cgy:%s " % e)
        raise e

def crawler_product_info(goon=False):
    count = 0
    driver = open_driver(1)
    if goon == True:
        try:
            url = r.get("rs_last_url")
            if url:
                r.rpush("rs_brand_url",url)
        except:
            print("error add last url:%s" % url)
    while True:
        try:
            url = r.rpop("rs_brand_url")
            if url == None:
                print("ok rs_brand_url empty")
                break
            r.set("rs_last_url",url)
            url = str(url, encoding = "utf-8")
            print("begin crawler brand:%s" % url)
            #url = "http://china.rs-online.com/web/b/abb/"
            #url = "http://china.rs-online.com/web/c/connectors/pcb-connectors/pcb-headers/?#applied-dimensions=4294967289"
            #url = "http://china.rs-online.com/web/c/hvac-fans-thermal-management/air-filters-accessories/hvac-air-filters/?#applied-dimensions=4294581234"
            count = parser_product_cgy(driver,url)
        except Exception as e: 
            re = test_ip('http://china.rs-online.com/web/b/abus/','ABUS')
            if re == False:
                switch_ip()
            r.lpush("rs_brand_url",url)
            close_driver(driver,1)
            driver = open_driver(1)
            print("error in crawler_product_info:%s %s" % (url,e))
    close_driver(driver,1)
