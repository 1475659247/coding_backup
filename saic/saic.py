from selenium import webdriver
import requests
import traceback
import time
from ua import *
from bs4 import BeautifulSoup
from pyvirtualdisplay import Display
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

#配置代理服务器认证
PROXY_USER = 'zrx70'
PROXY_PASSWD = '61197'
PROXY_IP = '222.184.35.196'
PROXY_PORT = '33180'

def open_driver():
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    
    dcap["phantomjs.page.settings.userAgent"] = (ua_list[random.randint(0, len(ua_list)-1)])
    _proxy = "--proxy=%s:%s" % (PROXY_IP,PROXY_PORT)
    _proxy_auth = "--proxy-auth=%s:%s" % (PROXY_USER,PROXY_PASSWD)
    service_args = [ _proxy,
                     _proxy_auth,
                     '--debug=true',
                    '--proxy-type=socks5',
                    '--ignore-ssl-errors=true',
                    '--load-images=yes',
                    '--disk-cache=no']
    driver = webdriver.PhantomJS('/usr/local/bin/phantomjs',service_args=service_args,desired_capabilities=dcap)
    #driver.set_page_load_timeout(10)
    #driver.set_script_timeout(10)
    return driver


def test():
    url = "http://wsjs.saic.gov.cn/"
    driver = open_driver()
    driver.get(url)
    time.sleep(5+random.random())
    driver.find_element_by_xpath('''//div[@class='centent']/div/ul/li/table/tbody/tr/td/div[p='商标状态查询']''').click()
    time.sleep(2+random.random())
    check_id = "7734676"
    driver.find_element_by_class_name('input').send_keys(check_id)
    #driver.find_element_by_xpath('''//*[@id="submitForm"]/div/div[1]/table/tbody/tr/td[2]/div/input''').send_keys(check_id)
    time.sleep(1+random.random())
    actions = ActionChains(driver)
    actions.key_down(Keys.TAB)
    actions.perform()
    time.sleep(2)
    actions.key_down(Keys.TAB)
    actions.perform()
    time.sleep(2)
    actions.key_down(Keys.TAB)
    actions.perform()
    driver.find_element_by_id('_searchButton').click()

    time.sleep(2)
    windows = driver.window_handles
    driver.switch_to_window(windows[1])
    time.sleep(10)
    driver.find_element_by_xpath('''//*[@id="list_box"]/table/tbody/tr[2]/td[2]/a''').click()
    driver.find_element_by_xpath('''/html/body/div[4]/div/ul/li[1]''')
    
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    print(soup.title)
    #close_driver(driver,0)

if __name__ == '__main__':
    test()
