from config.config import *
from map_list import *
import csv

driver_login = open_driver(0)
driver_http = open_driver(1)

wx_url = "http://t.wxb.com/media/all?keyword=&pageSize=10&page="

def login(username,passwd):
    driver_login.get(LOGIN_URL)
    driver_login.find_element_by_id("username").clear()
    driver_login.find_element_by_id("username").send_keys(username)
    time.sleep(2)
    driver_login.find_element_by_id("password").clear()
    driver_login.find_element_by_id("password").send_keys(passwd)
    time.sleep(2.5)
    driver_login.find_element_by_xpath('''//*[@id="loginForm"]/div[4]/button''').click()
    time.sleep(2)
    cookies = driver_login.get_cookies()
    for cookie in cookies:
        driver_http.cookies.set(cookie['name'], cookie['value'])
    '''
    url = "http://t.wxb.com/media/all?keyword=&pageSize=10&page=1"
    rsp = driver_http.get(url,headers=ua.get_ua(url)) 
    print(rsp.content.decode('utf-8'))
    '''

def get_wx_info():
    url = wx_url + '1'
    rsp = driver_http.get(url,headers=ua.get_ua(url)) 
    json_obj = json.loads(rsp.content.decode('utf-8'))
    totle_count = json_obj.get('totalCount')
    pg_f = lambda x:int(x/10) + (x%10 != 0)
    page_num = pg_f(int(totle_count))

    try:
        os.remove('f.txt')
    except:
        pass
    for page_id in range(1,page_num+1):
        url = wx_url + str(page_id)
        print(url)
        rsp = driver_http.get(url,headers=ua.get_ua(url)) 
        wx_info_str = rsp.content.decode('utf-8')
        f=open('f.txt','a')
        f.write(wx_info_str)
        f.write('\n\n')
        f.close

def parser_wx_csv():
    csvfile=open('wx.csv','w',encoding='utf8',newline='')
    spamwriter = csv.writer(csvfile,dialect='excel')
    spamwriter.writerow(['wx_name','wx_id','wx_desc','sex_male','sex_female','area_id','category_str',\
                'count_push_latest_30','count_article_latest_30','is_weixin_verify','raw_id',\
                'qrcode_url','fans_num','idx1_read_num_avg','avg_read_num_non_top','update_time'])
    f=open('f.txt','r')
    count = 0
    for line in f:
        if line =='\n':
            continue
        json_obj = json.loads(line)
        wx_list = json_obj.get('data')
        for wx in wx_list:
            try:
                wx_name = wx.get('wx_name')
            except:
                pass
            try:
                wx_id = wx.get('wx_id')
            except:
                pass
            try:
                wx_desc = wx.get('wx_desc')
            except:
                pass
            try:
                sex_male = wx.get('sex_male')
            except:
                pass
            try:
                sex_female = wx.get('sex_female')
            except:
                pass
            try:
                area_id = wx.get('area_id')
            except:
                pass
            try:
                category = wx.get('category')
                category_str = ''
                if category:
                    category_str = category_map[int(category)-1]
            except:
                pass
            try:
                count_push_latest_30 = wx.get('count_push_latest_30')
            except:
                pass
            try:
                count_article_latest_30 = wx.get('count_article_latest_30')
            except:
                pass
            try:
                is_weixin_verify = wx.get('is_weixin_verify')
            except:
                pass
            try:
                raw_id = wx.get('raw_id')
            except:
                pass
            try:
                qrcode_url = wx.get('qrcode_url')
            except:
                pass
            try:
                fans_num = wx.get('fans_num')
            except:
                pass
            try:
                idx1_read_num_avg = wx.get('idx1_read_num_avg')
            except:
                pass
            try:
                avg_read_num_non_top = wx.get('avg_read_num_non_top')
            except:
                pass
            try:
                update_time = wx.get('update_time')
            except:
                pass

            '''
            print(wx_name,wx_id,wx_desc,sex_male,sex_female,area_id,category_str,\
                count_push_latest_30,count_article_latest_30,is_weixin_verify,raw_id,\
                qrcode_url,fans_num,idx1_read_num_avg,avg_read_num_non_top,update_time)
            '''
            spamwriter.writerow([wx_name,wx_id,wx_desc,sex_male,sex_female,area_id,category_str,\
                count_push_latest_30,count_article_latest_30,is_weixin_verify,raw_id,\
                qrcode_url,fans_num,idx1_read_num_avg,avg_read_num_non_top,update_time])
            count +=1
            print(count)

def run(flag):
    if flag == '0':
        login(USERNAME,PASSWD)
        get_wx_info()
    elif flag == '1':
        parser_wx_csv()

'''
先执行python wxb.py 0 生成原生json文本f.txt
再执行python wxb.py 1 转成csv wxb.csv
'''
if __name__ == "__main__":
    flag = sys.argv[1]
    run(flag)
    close_driver(driver_login,0)
