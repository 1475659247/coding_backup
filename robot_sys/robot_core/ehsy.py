import requests
import traceback
from config.config import *
from config.ua import *
from sql_orm.orm import *
from bs4 import BeautifulSoup
import os
def get_category():
    ipproxy = 2
    index_url = ehsy_host + '/'
    while True:
        try:
            driver = open_driver(0,ipproxy=ipproxy)
            driver.get(index_url)
            time.sleep(3)
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            menu_soup = soup.find_all('a',attrs={"class":"aHref-level3 ng-binding"})
            count = 0;
            if len(menu_soup):
                break
        except:
            re = test_ip('http://www.ehsy.com/category-2249','综合套装')
            if re == False:
                switch_ip()
            close_driver(driver,0)
            print("retry get category")
            continue

    r.delete("ehsy_category_url")
    for link in menu_soup:
        url = ehsy_host + link.get('href')
        #print(url)
        r.lpush("ehsy_category_url",url)
        count +=1
    print("ok category:%d" % count)
    close_driver(driver,0)
    return count

def get_brand_url(brand_url):
    try:
        img_link = ''
        rsp = requests.get(brand_url,headers=get_ua(ehsy_brand_url))
        soup = BeautifulSoup(rsp.content, 'html.parser')
        main_soup = soup.find('div',attrs={"class":"mod-brand-logo"})
        img_link = main_soup.find('img').get('src')
    except Exception as e: 
        #print("%s" % traceback.print_exc())
        img_link = ''

    return img_link

def find_brand(brand_name):
    try:
        brand = None
        if brand_name == '':
            return brand
        brand_search = store_s.query(ParityBrand).filter(or_(ParityBrand.brand_zh_name == brand_name,ParityBrand.brand_en_name == brand_name)).first()
        if brand_search:
            brand = brand_search
    except Exception as e: 
        print("%s" % traceback.print_exc())
    return brand

def update_site():
    parity_site = store_s.query(ParitySite).filter(ParitySite.site_id == EHSY_ID).first()
    if parity_site:
        parity_site.site_name = ehsy_name
        parity_site.site_type = ehsy_site_type
        parity_site.site_telephone = ehsy_telephone
        parity_site.site_logo = ehsy_logo_path
        parity_site.site_web = ehsy_host
        parity_site.status = 0
    else:
        parity_site = ParitySite()
        parity_site.site_id = EHSY_ID
        parity_site.site_name = ehsy_name
        parity_site.site_type = ehsy_site_type
        parity_site.site_telephone = ehsy_telephone
        parity_site.site_logo = ehsy_logo_path
        parity_site.site_web = ehsy_host
        parity_site.status = 0
        store_s.add(parity_site)
    store_s.commit()
    
def down_brand_img():
    root_path = 'brand'
    if os.path.exists(root_path) == False:
        os.makedirs(root_path)
    brand_list = store_s.query(ParityBrand).all()
    for brand in brand_list:
        if brand.brand_logo_url == '':
            continue
        dir_path = 'brand'  + '/' + str(brand.brand_id) + '/'
        if os.path.exists(dir_path) == False:
            os.makedirs(dir_path)
        img_url = brand.brand_logo_url
        try:
            img_name = brand.brand_logo
            if os.path.isfile(img_name) == True:
                continue
            rsp = requests.get(img_url,headers=get_ua(img_url),timeout=5)
            with open(img_name, "wb") as code:
                code.write(rsp.content)
        except Exception as e: 
            print("error down img:%s %s" % (img_url,e))
            continue

def update_brand():
    try:
        rsp = requests.get(ehsy_brand_url,headers=get_ua(ehsy_brand_url))
        soup = BeautifulSoup(rsp.content, 'html.parser')
        main_soup = soup.find('div',attrs={"class":"brand-table"})
        links = main_soup.find_all('a')
        count = 0;
        for link in links:
            try:
                parity_brand = ParityBrand()
                brand_url = link.get('href')
                if '/brand' not in brand_url:
                    continue
                brand_url = ehsy_host + brand_url
                brand_str = link.text.replace('\n','').replace('\r','').strip()[0:255]
                try:
                    brand_zh_name = brand_str.split('/')[0]
                    if '国产' in brand_zh_name:
                        brand_zh_name = "国产"
                    uchar = brand_zh_name[0]
                    uchar2 = brand_zh_name[-1]
                    if (uchar < u'\u4e00' or uchar > u'\u9fa5') and (uchar2 < u'\u4e00' or uchar2 > u'\u9fa5'):
                        raise Exception
                    else:
                        parity_brand.brand_zh_name = brand_zh_name
                except:
                    parity_brand.brand_zh_name = ''

                try:
                    brand_en_name = brand_str.split('/')[-1]
                    uchar = brand_en_name[0]
                    if ('\u0041' <= uchar<='\u005a') or ('\u0061' <= uchar<='\u007a') or ('0' <= uchar <= '9'):
                        parity_brand.brand_en_name = brand_en_name
                    else:
                        parity_brand.brand_en_name = ''
                except:
                    parity_brand.brand_en_name = ''

                brand_logo_url = get_brand_url(brand_url)
                parity_brand.brand_logo_url = brand_logo_url


                if DEBUG_LEVEL != 0:
                    print(parity_brand)
                brand_search = find_brand(brand_zh_name)
                brand_search_en = find_brand(brand_en_name)
                if brand_search:
                    if brand_search.brand_en_name == '':
                        brand_search.brand_en_name = parity_brand.brand_en_name
                    if brand_search.brand_logo == '':
                        if parity_brand.brand_logo_url != '': 
                            dir_path = 'brand'  + '/' + str(brand_search.brand_id) + '/'
                            parity_brand.brand_logo = dir_path + str(brand_search.brand_id) + '.' + parity_brand.brand_logo_url.split('.')[-1]
                            brand_search.brand_logo = parity_brand.brand_logo
                            brand_search.brand_logo_url = parity_brand.brand_logo_url
                    store_s.commit()
                elif brand_search_en: 
                    if brand_search_en.brand_zh_name == '':
                        brand_search_en.brand_zh_name = parity_brand.brand_zh_name
                    if brand_search_en.brand_logo == '':
                        if parity_brand.brand_logo_url != '': 
                            dir_path = 'brand'  + '/' + str(brand_search_en.brand_id) + '/'
                            parity_brand.brand_logo = dir_path + str(brand_search_en.brand_id) + '.' + parity_brand.brand_logo_url.split('.')[-1]
                            brand_search_en.brand_logo = parity_brand.brand_logo
                            brand_search_en.brand_logo_url = parity_brand.brand_logo_url
                    store_s.commit()
                else:
                    brand_search = store_s.query(ParityBrand).order_by(ParityBrand.brand_id.desc()).first()
                    if brand_search:
                        count = brand_search.brand_id
                    else:
                        count = 10000
                    parity_brand.brand_id = count + 1
                    if parity_brand.brand_logo_url != '':
                        dir_path = 'brand'  + '/' + str(parity_brand.brand_id) + '/'
                        parity_brand.brand_logo = dir_path + str(parity_brand.brand_id) + '.' + parity_brand.brand_logo_url.split('.')[-1]
                    store_s.add(parity_brand)
                    store_s.commit()
            except Exception as e: 
                print("%s" % traceback.print_exc())
                continue 
        print("ok brand :count=%d"% count)

    except Exception as e: 
        print("%s" % traceback.print_exc())

def test():
    #display = Display(visible=0, size=(800, 600))
    #display.start()
    url = "http://www.ehsy.com/category-12159"
    driver = open_driver(0)
    html = http_get(url,driver,0)
    soup = BeautifulSoup(html, 'html.parser')
    print(soup.title)
    close_driver(driver,0)
    #display.stop()
