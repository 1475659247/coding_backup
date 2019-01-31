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
    parity_site = store_s.query(ParitySite).filter(ParitySite.site_id == VIPMRO_ID).first()
    if parity_site:
        parity_site.site_name = vipmro_name
        parity_site.site_type = vipmro_site_type
        parity_site.site_telephone = vipmro_telephone
        parity_site.site_logo = vipmro_logo_path
        parity_site.site_web = vipmro_host
        parity_site.status = 0
    else:
        parity_site = ParitySite()
        parity_site.site_id = VIPMRO_ID
        parity_site.site_name = vipmro_name
        parity_site.site_type = vipmro_site_type
        parity_site.site_telephone = vipmro_telephone
        parity_site.site_logo = vipmro_logo_path
        parity_site.site_web = vipmro_host
        parity_site.status = 0
        store_s.add(parity_site)
    store_s.commit()
    
def update_brand(html):
    brand_id = 0
    soup = BeautifulSoup(html, 'html.parser')
    #update brand
    try:
        main_soup = soup.find('label',attrs={"class":"J_nameCn"})
        brand_zh_name = main_soup.text.strip()
        uchar = brand_zh_name[0]
        uchar2 = brand_zh_name[-1]
        if (uchar < u'\u4e00' or uchar > u'\u9fa5') and (uchar2 < u'\u4e00' or uchar2 > u'\u9fa5'):
            raise Exception
        for ft in vipmro_str:
            brand_zh_name = brand_zh_name.split(ft)[0]
    except:
        brand_zh_name = ''

    try:
        main_soup = soup.find('label',attrs={"class":"J_nameEn"})
        brand_en_name = main_soup.text.strip()
        uchar = brand_en_name[0]
        if ('\u0041' <= uchar<='\u005a') or ('\u0061' <= uchar<='\u007a') or ('0'<=uchar<='9'):
            brand_en_name = brand_en_name
        else:
            brand_en_name = ''
    except:
            brand_en_name = ''
    if brand_zh_name == '' and brand_en_name == '':
        return brand_id

    try:
        main_soup = soup.find('div',attrs={"class":"brand-detail-top-b J_logo"})
        sub_soup = main_soup.find('img')
        brand_logo_url = sub_soup.get("src")
    except Exception as e: 
        brand_logo_url = ''
    
    brand_search = ehsy.find_brand(brand_zh_name)
    brand_search_en = ehsy.find_brand(brand_en_name)
    if brand_search:
        brand_id = brand_search.brand_id
        if brand_search.brand_en_name == '':
            brand_search.brand_en_name = brand_en_name
        if brand_search.brand_logo == '':
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

def parser_product(driver,url):
    try:
        count = 0
        driver.get(url)
        h4 = WebDriverWait(driver, 10).until(\
                               EC.presence_of_element_located((By.CLASS_NAME, 'brand-detail-body-pro')))
        time.sleep(2)
        html = driver.page_source
        brand_id = update_brand(html)
        if brand_id == 0:
            return count
        while True:
            soup = BeautifulSoup(html, 'html.parser')
            main_soup = soup.find('ul',attrs={"class":"J_brandList"})
            sub_soup = main_soup.find_all('li')
            if len(sub_soup) == 0:
                #print("error get product li")
                raise Exception
            for product in sub_soup:
                try:
                    soup_t = product.find('a',attrs={"class":"a"})
                    name = soup_t.text.strip()
                    product_url = soup_t.get("href")
                    product_id = 'VIPMRO' + product_url.split('/')[-1]
                except Exception as e: 
                    raise Exception
                #
                try:
                    soup_t = product.find('span',attrs={"class":"a"})
                    #model = soup_t.text.split(':')[-1].split('|')[0].strip()
                    model = soup_t.text.split('|')[0].replace("型号：",'').strip()
                except:
                    model = ''
                #
                site_id = VIPMRO_ID
                #
                try:
                    soup_t = product.find('label',attrs={"class":"a"})
                    price = soup_t.text.split('¥')[-1].replace('\n','').replace('\r','').strip()
                    price = ("%.3f" % float(''.join(price.split(','))))
                    price = decimal.Decimal(price)
                except:
                    price = decimal.Decimal(0.000)

                #
                try:
                    soup_t = product.find('span',attrs={"class":"d"})
                    goods_time = soup_t.find('label').text.strip()
                    goods_time = int(''.join(list(filter(str.isdigit,goods_time))))
                    goods_time = int(goods_time)
                except:
                    goods_time = 0
                #
                try:
                    soup_t = product.find('span',attrs={"class":"c"})
                    sales = soup_t.find_all('label')[1].text.strip()
                    sales = int(''.join(list(filter(str.isdigit,sales))))
                except:
                    sales = 0
                #
                try:
                    image_url = product.find('img').get('src')
                except:
                    image_url = ''
                   
                if image_url !='':
                    dir_path = 'vipmro/'
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
                        parity_product.type = vipmro_site_type
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
                        parity_product.type = vipmro_site_type
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
            try:
                option = driver.find_element_by_xpath("//div[@class='list-page J_page']/a[text()='下一页']")
                option.click()
                time.sleep(4)
                html = driver.page_source
                print("next_page...")
                continue
            except:
                print("ok product %s count:%d " % (url,count))
                return count
    except Exception as e:
        raise e

def crawler_product_info():
    ipproxy = 2
    driver = open_driver(0,ipproxy=ipproxy)
    while True:
        try:
            url = r.rpop("vipmro_brand_url")
            if url == None:
                print("ok vipmro_brand_url empty")
                break
            url = str(url, encoding = "utf-8")
            #url = "http://www.vipmro.com/brand/104"
            count = parser_product(driver,url)
        except Exception as e: 
            re = test_ip(url,'品牌详情页')
            if re == False:
                switch_ip()
                r.lpush("vipmro_brand_url",url)
            close_driver(driver,0)
            driver = open_driver(0,ipproxy=ipproxy)
            print("error crawler_product_info:%s %s" % (url,e))

def crawler_brand_url():
    r.delete("vipmro_brand_url")
    ipproxy = 2
    while True:
        try:
            driver = open_driver(0,ipproxy=ipproxy)
            driver.get(vipmro_brand_url)
            h4 = WebDriverWait(driver, 10).until(\
                                   EC.presence_of_element_located((By.CLASS_NAME, 'brand-all-top-eval')))
            time.sleep(3)
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            main_soup = soup.find('div',attrs={"class":"brand-all-top-eval"})
            links = main_soup.find_all('li')
            count = 0;
            if len(links) == 0:
                raise Exception
            for link in links:
                brand_link = link.find('a').get("href") 
                r.lpush("vipmro_brand_url",brand_link)
                count +=1
            if count != 0:
                print("ok brand :count=%d"% count)
                close_driver(driver,0)
                break
        except Exception as e: 
            re = test_ip('http://vipmro.com/product/569431','施耐德')
            if re == False:
                switch_ip()
            close_driver(driver,0)
            print("error retry crawler brand %s" % e)

def update_brand_cgy(brand_name):
    brand_id = 0
    brand_en_name = ''
    #update brand
    try:
        if ')' in brand_name:
            brand_zh_name = brand_name.split('(')[0]
            brand_en_name = brand_name.split('(')[-1].split(')')[0]
        elif '）' in brand_name:
            brand_zh_name = brand_name.split('（')[0]
            brand_en_name = brand_name.split('（')[-1].split('）')[0]
        elif '】' in brand_name:
            brand_zh_name = brand_name.split('】')[0].replace('【','').replace('】','')
            for ft in vipmro_str:
                brand_zh_name = brand_name.split(ft)[0]
        else:
            brand_zh_name = brand_name

    except Exception as e: 
        print("error parser brand_name:%s" % e)
        return brand_id

    try:
        uchar = brand_zh_name[0]
        uchar2 = brand_zh_name[-1]
        if (uchar < u'\u4e00' or uchar > u'\u9fa5') and (uchar2 < u'\u4e00' or uchar2 > u'\u9fa5'):
            raise Exception
        for ft in vipmro_str:
            brand_zh_name = brand_zh_name.split(ft)[0]
    except:
        brand_en_name = brand_zh_name
        brand_zh_name = ''
    try:
        uchar = brand_en_name[0]
        if ('\u0041' <= uchar<='\u005a') or ('\u0061' <= uchar<='\u007a') or ('0'<=uchar<='9'):
            brand_en_name = brand_en_name
        else:
            brand_en_name = ''
    except:
        brand_en_name = ''
    if brand_zh_name == '' and brand_en_name == '':
        return brand_id
    brand_search = ehsy.find_brand(brand_zh_name)
    brand_search_en = ehsy.find_brand(brand_en_name)
    if brand_search:
        brand_id = brand_search.brand_id
    elif brand_search_en: 
        brand_id = brand_search_en.brand_id
    else:
        brand_search = store_s.query(ParityBrand).order_by(ParityBrand.brand_id.desc()).first()
        if brand_search:
            count = brand_search.brand_id
        else:
            count = 10000
        parity_brand = ParityBrand()
        parity_brand.brand_zh_name = brand_zh_name
        parity_brand.brand_en_name = brand_en_name
        parity_brand.brand_logo_url = ''
        parity_brand.brand_logo = ''
        parity_brand.brand_id = count + 1
        brand_id = parity_brand.brand_id
        store_s.add(parity_brand)
        store_s.commit()
    return brand_id

def parser_product_cgy(url):
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
            main_soup = soup.find('div',attrs={"class":"list-main-box J_list J_car_box"})
            sub_soup = main_soup.find_all('li')
            if last_product in sub_soup:
                print("Warning hit same...")
                switch_ip()
                raise Exception
            else:
                last_product = sub_soup[-1]
            if len(sub_soup) == 0:
                #print("error get product li")
                raise Exception
            for product in sub_soup:
                try:
                    soup_t = product.find('span',attrs={"class":"title"})
                    name = soup_t.text.strip()
                    soup_t = product.find('a')
                    product_url = soup_t.get("href")
                    product_id = 'VIPMRO' + product_url.split('/')[-1]
                except Exception as e: 
                    raise Exception
                #
                brand_name = name.split(' ')[0]
                brand_id = update_brand_cgy(brand_name)
                if brand_id == 0:
                    continue
                #
                try:
                    soup_t = product.find('span',attrs={"class":"model m-top5"})
                    model = soup_t.text.replace("商品型号：",'').strip()
                except:
                    model = ''
                #
                site_id = VIPMRO_ID
                #
                try:
                    soup_t = product.find('font',attrs={"class":"weight ft14"})
                    price = soup_t.text.split('¥')[-1].replace('\n','').replace('\r','').strip()
                    price = ("%.3f" % float(''.join(price.split(','))))
                    price = decimal.Decimal(price)
                except:
                    price = decimal.Decimal(0.000)

                #
                goods_time = 0

                #
                try:
                    soup_t = product.find('font',attrs={"class":"fr"})
                    sales = soup_t.text.strip()
                    sales = int(''.join(list(filter(str.isdigit,sales))))
                except:
                    sales = 0
                #
                try:
                    image_url = product.find('img').get('src')
                except:
                    image_url = ''
                   
                if image_url !='':
                    dir_path = 'vipmro/'
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
                        parity_product.type = vipmro_site_type
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
                        parity_product.type = vipmro_site_type
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
                    count = count+1
                except Exception as e:
                    print("error commit:%s %s" % (e,parity_product))
                    raise e
            try:
                option = driver.find_element_by_xpath("//div[@class='list-page J_page']/a[text()='下一页']")
                option.click()
                time.sleep(3)
                html = driver.page_source
                print("next_page...")
                continue
            except:
                print("ok product %s count:%d " % (url,count))
                close_driver(driver,0)
                return count
    except Exception as e:
        close_driver(driver,0)
        raise e

def crawler_product_info_cgy():
    while True:
        try:
            url = r.rpop("vipmro_category_url")
            if url == None:
                print("ok vipmro_category_url empty")
                break
            url = str(url, encoding = "utf-8")
            #url = "http://vipmro.com/search?categoryId=501012"
            count = parser_product_cgy(url)
        except Exception as e: 
            re = test_ip(url,'列表页')
            if re == False:
                switch_ip()
            r.lpush("vipmro_category_url",url)
            print("error crawler_category_info:%s %s" % (url,e))

def crawler_category_url():
    ipproxy = 2
    r.delete("vipmro_category_url")
    while True:
        try:
            driver = open_driver(0,ipproxy=ipproxy)
            driver.get(vipmro_host)
            h4 = WebDriverWait(driver, 5).until(\
                                    EC.presence_of_element_located((By.CLASS_NAME, 'nav-main-type')))
            time.sleep(3)
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            menu_soup = soup.find_all('div',attrs={"class":"nav-main-type"})
            count = 0;
            if len(menu_soup) == 0:
                raise Exception
            for link_soup in menu_soup:
                try:
                    sub_soup = link_soup.find_all('li')
                    for link in sub_soup:
                        url = link.find('a').get('href')
                        print(url)
                        r.lpush("vipmro_category_url",url)
                        count +=1
                except Exception as e:
                    print("error get_category failed %s" % link_soup)
                    continue
            if count != 0:
                print("ok category :count=%d"% count)
                close_driver(driver,0)
                break
        except Exception as e: 
            re = test_ip('http://vipmro.com/product/569431','施耐德')
            if re == False:
                switch_ip()
            close_driver(driver,0)
            print("error retry crawler category %s" % e)


def test():
    ipproxy = 2
    url = "http://vipmro.com/product/569431"
    switch_ip()
    re = test_ip('http://vipmro.com/search?categoryId=501110','列表页')
    if re == True:
        print("ip is ok")
    driver = open_driver(0,ipproxy=ipproxy)
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    print(soup.title)
    close_driver(driver,0)

