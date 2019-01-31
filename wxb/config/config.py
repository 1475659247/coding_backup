from . import ua
from selenium import webdriver
import random
import time
import json
import os
import sys
import requests
from pyvirtualdisplay import Display
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
display = Display(visible=0, size=(800, 600))
display.start()
from pyvirtualdisplay import Display

LOGIN_URL = 'https://account.wxb.com/?from=http%3A%2F%2Ft.wxb.com'
USERNAME = '18271843933'
PASSWD = 'haha123'

#配置代理服务器认证
PROXY_USER = '***'
PROXY_PASSWD = '***'
PROXY_IP = '222.184.35.196'
PROXY_PORT = '33180'

proxyMeta = "socks5://%(user)s:%(pass)s@%(host)s:%(port)s" % {
        "host" : PROXY_IP,
        "port" : PROXY_PORT,
        "user" : PROXY_USER,
        "pass" : PROXY_PASSWD,
    }

proxies = {
    "http" : proxyMeta,
    "https" : proxyMeta,
}

def open_driver(mode,ipproxy=0):
    if mode == 1:
        driver = requests.session()
    elif mode == 0:
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        
        dcap["phantomjs.page.settings.userAgent"] = (ua.ua_list[random.randint(0, len(ua.ua_list)-1)])
        if ipproxy == 1:
            rsp = requests.get("http://127.0.0.1:8000/select?name=vipmro&anonymity=2&order=speed&count=20") 
            json_list = str(rsp.content,encoding='utf-8')
            ip_list = json.loads(json_list)
            ip_proxy  = ip_list[random.randint(0,len(ip_list))-1]
            ip = ip_proxy.get('ip')
            port = ip_proxy.get('port')
            __proxy = '--proxy=' + ip + ':' + str(port)
            service_args = [ __proxy,
                            '--proxy-type=http',
                            '--ignore-ssl-errors=true',
                            '--load-images=no',
                            '--disk-cache=yes']
            driver = webdriver.PhantomJS('/usr/local/bin/phantomjs',service_args=service_args,desired_capabilities=dcap)
            driver.set_page_load_timeout(10)
            driver.set_script_timeout(10)
        elif ipproxy == 2:
            _proxy = "--proxy=%s:%s" % (PROXY_IP,PROXY_PORT)
            _proxy_auth = "--proxy-auth=%s:%s" % (PROXY_USER,PROXY_PASSWD)
            service_args = [ _proxy,
                             _proxy_auth,
                            '--proxy-type=socks5',
                            '--ignore-ssl-errors=true',
                            '--load-images=no',
                            '--disk-cache=yes']
            driver = webdriver.PhantomJS('/usr/local/bin/phantomjs',service_args=service_args,desired_capabilities=dcap)
            driver.set_page_load_timeout(10)
            driver.set_script_timeout(10)
        elif ipproxy == 3:
            service_args = ['--ignore-ssl-errors=true',
                            '--load-images=no',
                            '--disk-cache=yes']
            driver = webdriver.PhantomJS('/usr/local/bin/phantomjs',service_args=service_args,desired_capabilities=dcap)
            driver.set_page_load_timeout(10)
            driver.set_script_timeout(10)
        else:
            driver =webdriver.Chrome('chromedriver')
            driver.set_page_load_timeout(10)
            driver.set_script_timeout(10)
            driver.set_window_size(1920, 1080)

    return driver

def close_driver(driver,mode):
    if mode == 0:
        driver.quit()

def http_get(url,driver,mode,time_out=None,proxies=None):
    #print("process:%s "% url)
    if mode == 1:
        headers = ua.get_ua(url)
        #print(headers)
        try:
            if time_out:
                rsp = driver.get(url,headers=headers,timeout=time_out,proxies=proxies)
            else:
                rsp = driver.get(url,headers=headers,proxies=proxies)
            return rsp.content
        except Exception as e:
            print("error http_get %s %s" % (url,e))
            return None
    elif mode == 0:
        try:
            if time_out:
                driver.set_page_load_timeout(time_out)
            driver.get(url)
            html = driver.page_source
            return html
        except Exception as e:
            print("error http_get %s" % e)
            html = driver.page_source
            return html

def test_ip(url=None,key=None,time_out=5):
    try:
        ipproxy = 2
        if url == None:
            url = "https://www.baidu.com/"
        if key == None:
            key = '百度'
        driver = open_driver(0,ipproxy=ipproxy)
        try:
            driver.get(url)
            time.sleep(time_out)
        except:
            pass
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        #print(soup.title.text)
        if key in soup.title.text:
            close_driver(driver,0)
            return True
        else:
            close_driver(driver,0)
            return False
    except Exception as e:
        print("error test ip:%s " % e)
        close_driver(driver,0)
        return False

def switch_ip():
    count = 0
    re = r.get("ip_status")
    if re == None:
        r.setex("ip_status","switching",120)
        while True:
            try:
                url = "http://ip.hahado.cn/simple/switch-ip?username=%s&password=%s" \
                    % (PROXY_USER,PROXY_PASSWD)
                rsp = requests.get(url,timeout=10) 
                json_list = str(rsp.content,encoding='utf-8')
                ip_list = json.loads(json_list)
                last_ip = ip_list[0].get('last_ip')
                #print("last_ip:%s" % last_ip)

                while True:
                    url = "http://ip.hahado.cn/simple/current-ip?username=%s&password=%s" \
                        % (PROXY_USER,PROXY_PASSWD)
                    rsp = requests.get(url,timeout=10) 
                    json_list = str(rsp.content,encoding='utf-8')
                    ip_list = json.loads(json_list)
                    new_ip = ip_list[0].get('ip')
                    #print("new_ip:%s" % new_ip)
                    if new_ip == last_ip or new_ip == None:
                        count +=1
                        print("switching ip...")
                        time.sleep(4)
                        if count > 10:
                            break
                    else:
                        break

                while True:
                    print("test ip...")
                    re = test_ip()
                    if re == True:
                        time_ = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                        print("switch ip:%s %s" % (time_,new_ip))
                        break
                break
            except Exception as e:
                print("retry switch ip %s" % e)
                time.sleep(20)
    else:
        print("other crawler switching ip... ")
        time.sleep(30)
