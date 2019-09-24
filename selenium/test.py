# -*- coding: utf-8 -*-

import requests
import time
import random
from lxml import etree
# 接打码平台
from dama import YDMHttp
def get_responses():
    """获得页面信息
    """
    myCookies = dict(WebBrokerSessionID = 't9bipDvVOYZ8pzZC')
    url = 'https://toefl.etest.net.cn/cn/ScoreReport?AppID=1542028'  
    r = requests.get(url = url , cookies = myCookies).content
    print r
    with open("2.html" ,"w") as f:
        f.write(r)
    return r

def get_detail(html):
    # 解析html 为 HTML 文档
    selector=etree.HTML(html)
    text = selector.xpath('//*[@id="maincontent"]/table[1]//td/text()')
    for t in text:
        print t
    test_data =  selector.xpath('//*[@id="maincontent"]/table[1]/tbody/tr[2]/td[2]/text()') 
    print text,test_data
def loginin():
    picUrl = "http://toefl.etest.net.cn/cn/"+ str(int(time.time()*1000))+str(random.random())+"VerifyCode3.jpg"
    
    payload = {"username":"1281490","__act":"__id.24.TOEFLAPP.appadp.actLogin","password":"9253579F17ac","LoginCode":"plk4","submit.x":"32","submit.y":"9"}
    r = requests.post("http://toefl.etest.net.cn/cn/TOEFLAPP",data=payload)
    with open("3.html" ,"w") as f:
        f.write(r.content)
# r = get_responses()
# get_detail(r)
loginin()
