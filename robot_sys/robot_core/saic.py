import requests
import traceback
from robot_core import ehsy
from config.config import *
from config.ua import *
from sql_orm.orm import *
from bs4 import BeautifulSoup
import os
import decimal

def test():
    ipproxy = 2
    url = "http://wsjs.saic.gov.cn/"
    driver = open_driver(0,ipproxy=ipproxy)
    driver.get(url)
    #time.sleep(random.random())
    time.sleep(3+random.random())
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

