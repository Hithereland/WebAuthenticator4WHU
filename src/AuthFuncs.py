import requests as rq
import time
import re


my_try_url = 'http://baidu.com'


# http is necessary, https is not suitable for WHU, HA HA HA HA HA HA

def get_auth_url(try_url: str = my_try_url) -> str:
    failed_times = 0
    status_code = 0
    rcv = rq.Response
    try:
        rcv = rq.get(try_url, timeout=1)
    except rq.exceptions.RequestException:
        failed_times += 1

    try:
        status_code = rcv.status_code
    except BaseException:
        status_code = 0

    while status_code != 200:
        time.sleep(3)
        failed_times += 1
        try:
            rcv = rq.get(try_url, timeout=1)
        except rq.exceptions.RequestException:
            failed_times = failed_times
        try:
            status_code = rcv.status_code
        except BaseException:
            status_code = 0

        if failed_times >= 20:
            return 'Error'

    ret = re.search("\'[\\s\\S]+\'", rcv.text).group(0)[1:-1]
    return ret


'''
    '%253D' : '='
    '%2526' : '&'

    userId=xxx&
    password=xxx&
    service=Internet&
    queryString=
    
    wlanuserip%253Dc24494995bbd9f7a6bc6ef87722efb29%2526
    wlanacname%253D29185648f4390d7911ef4b72391e17a9%2526
    ssid%253D%2526
    nasip%253D07e38f2323f330cd5ffcc3a203a63100%2526
    snmpagentip%253D%2526
    mac%253Dd5bc1014c80998dc1ae1e25965d5c228%2526
    t%253Dwireless-v2%2526
    url%253D4907361da15a6e864d2d1754aa4777b472c67de9b4494a00%2526
    apmac%253D%2526
    nasid%253D29185648f4390d7911ef4b72391e17a9%2526
    vid%253Dc4d938f8c9d81918%2526
    port%253De65ae3d6b3555e50%2526
    nasportid%253Dac41d60d7f1382081362a1ed29e6af2737b5a02181d45bf13c323bc515e5fe85
    &
    operatorPwd=&
    operatorUserId=&
    validcode=&
    passwordEncrypt=false
'''

'''
    what we can get in our URL

    http://172.19.1.9:8080/eportal/index.jsp?

    wlanuserip=c24494995bbd9f7a6bc6ef87722efb29&
    wlanacname=29185648f4390d7911ef4b72391e17a9&
    ssid=&
    nasip=07e38f2323f330cd5ffcc3a203a63100&
    snmpagentip=&
    mac=d5bc1014c80998dc1ae1e25965d5c228&
    t=wireless-v2&
    url=4907361da15a6e864d2d1754aa4777b472c67de9b4494a00&
    apmac=&
    nasid=29185648f4390d7911ef4b72391e17a9&
    vid=c4d938f8c9d81918&
    port=e65ae3d6b3555e50&
    nasportid=ac41d60d7f1382081362a1ed29e6af2737b5a02181d45bf13c323bc515e5fe85
'''


def make_post_data(auth_url: str, user_info: dict) -> str:
    query_string = re.search("\?[\\s\\S]+", auth_url).group(0)[1:].replace("=", "%253D").replace("&", "%2526")

    ret = "userId=" + str(user_info['userId']) + "&" + \
          "password=" + str(user_info['passwd']) + "&" + \
          "service=Internet&queryString=" + query_string + \
          "&operatorPwd=&operatorUserId=&validcode=&passwordEncrypt=false"

    return ret


'''
POST /eportal/InterFace.do?method=login HTTP/1.1 
Host: 172.19.1.9:8080 
Connection: keep-alive 
Content-Length: 641 
User-Agent: Mozilla/5.0 (Linux; Android 10; JEF-AN00 Build/HUAWEIJEF-AN00;) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/88.0.4324.93 Mobile Safari/537.36 
Content-Type: application/x-www-form-urlencoded; charset=UTF-8 
Accept: */* 
Origin: http://172.19.1.9:8080 
X-Requested-With: mark.via 
Referer: http://172.19.1.9:8080/eportal/index.jsp?wlanuserip=c24494995bbd9f7a6bc6ef87722efb29&wlanacname=29185648f4390d7911ef4b72391e17a9&ssid=&nasip=07e38f2323f330cd5ffcc3a203a63100&snmpagentip=&mac=d5bc1014c80998dc1ae1e25965d5c228&t=wireless-v2&url=4907361da15a6e864d2d1754aa4777b472c67de9b4494a00&apmac=&nasid=29185648f4390d7911ef4b72391e17a9&vid=c4d938f8c9d81918&port=e65ae3d6b3555e50&nasportid=ac41d60d7f1382081362a1ed29e6af2737b5a02181d45bf13c323bc515e5fe85 
Accept-Encoding: gzip, deflate 
Accept-Language: zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7 
'''


def login_and_auth(post_data: str, auth_url: str) -> (int, str):
    # build header
    header = {'Host': '172.19.1.9:8080',
              'Connection': 'keep-alive',
              'Content-Length': str(114514),
              'User-Agent': 'Mozilla/5.0',
              'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
              'Accept': '*/*',
              'Origin': 'http://172.19.1.9:8080',
              'Referer': auth_url,
              'Accept-Encoding': 'gzip, deflate',
              'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'}

    rcv = rq.post(url="http://172.19.1.9:8080/eportal/InterFace.do?method=login", data=post_data, headers=header)
    rcv.encoding = rcv.apparent_encoding
    return rcv.status_code, rcv.text

