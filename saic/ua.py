import random
ua_list = [
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0",
    "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) Gecko/20100101 Firefox/47.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:47.0) Gecko/20100101 Firefox/47.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:47.0) Gecko/20100101 Firefox/47.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.17",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.17",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.17",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.17",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.17",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.17",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.17",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.17",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.17",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36"]
def get_ua(url):
    host = url.split('/')[2]
    return {'Host': host,
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, sdch',
            'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
            'If-None-Match':'''W/"f7f88-3PhcGMQfGTJiAKTUd2Wdaw"''',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'Upgrade-Insecure-Requests':'1',  
            'User-Agent': ua_list[random.randint(0, len(ua_list)-1)]
            #'User-Agent': ua_list[-1]
            }
