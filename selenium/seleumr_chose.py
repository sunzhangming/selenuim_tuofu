# -*- coding: utf-8 -*-

import json
from urlparse import parse_qs
from wsgiref.simple_server import make_server



from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
# 滚动函数
from selenium.webdriver.common.action_chains import ActionChains
# 代理函数
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.proxy import ProxyType
from selenium.webdriver.common.proxy import Proxy
import csv
import time
import re
# 接打码平台
from dama_chose import YDMHttp
import sys
reload(sys)
sys.setdefaultencoding('utf8')


class Touful(object):
    def __init__(self):
        # chrome_options = Options()
        # chrome_options.add_argument("--proxy-server=http://120.77.35.48:8899")
        # chrome_options.add_argument("--headless")
        # self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.driver = webdriver.PhantomJS()
        self.driver.get("http://httpbin.org/ip")
        print(self.driver.page_source)
        self.error_list = [] # 爬取失败的城市
        # 链接mongo
        # client = MongoClient('主机ip',端口)
        self.aim_clear_api = None

    def open_url(self):
        """获取浏览器对象"""
        # get方法会一直等到页面被完全加载，然后才会继续程序，通常测试会在这里选择 time.sleep(2)
        self.driver.get("https://toefl.etest.net.cn/cn/")
        print "成功打开托福网站"
        time.sleep(2)

    def login(self):
        """登录"""
        self.driver.find_element_by_id("id_username").clear()
        self.driver.find_element_by_id("id_pwd").clear()
        self.driver.find_element_by_id("id_username").send_keys(u"1281490")
        self.driver.find_element_by_id("id_pwd").send_keys(u"Zengyichao!123")
        self.driver.find_element_by_id("a_changeone").click()
        time.sleep(2)
        self.driver.save_screenshot("tuoful_chose.png")  # 截取当前页面全图
        element = self.driver.find_element_by_id("imgVerifycode")  # 验证码的按钮
        # 计算出元素上、下、左、右 位置
        left = element.location["x"]
        top = element.location["y"]
        right = element.location["x"] + element.size["width"]
        bottom = element.location["y"] + element.size["height"]
        im = Image.open("tuoful_chose.png")
        # im = im.crop((232.0, 287.0, 322.0, 322.0))
        im = im.crop((int(left), int(top), int(right), int(bottom)))
        im.save("yz_chose.png")
        # codeContent = raw_input("读取验证码内容：")#临时
        codeContent = YDMHttp().start()  # 云打码
        self.driver.find_element_by_name("LoginCode").send_keys(codeContent)
        self.driver.find_element_by_id("id_login").click()
        time.sleep(2)
        content = self.driver.page_source
        if "我的首页" in content:
            return True
        else:
            return False

    def search_zuowei(self):
        """查询空置考场"""
        self.driver.find_element_by_link_text("考位查询").click()

    def month(self, month):
        """返回一个月份"""
        self.driver.find_elements_by_xpath('//input[@value="%s"]' % month)[0].click()

    def are(self, are):
        """返回一个地区"""
        self.driver.find_elements_by_xpath('//input[@value="%s"]' % are)[0].click()

    def get_zuowei(self):
        """得到一个月的一个地区的考场信息"""
        scroll_add_crowd_button = self.driver.find_element_by_id("footer")
        self.driver.execute_script("arguments[0].scrollIntoView();", scroll_add_crowd_button)
        time.sleep(3)
        self.driver.save_screenshot("tuoful_chose.png")  # 截取当前页面全图
        im = Image.open("tuoful_chose.png")
        im = im.crop((314.0, 377.0, 404.0, 412.0))
        im.save("yz_chose.png")
        # codeContent2 = raw_input("读取验证码内容：")#临时
        codeContent2 = YDMHttp().start()
        self.driver.find_element_by_name("afCalcResult").send_keys(codeContent2)
        time.sleep(2)
        self.driver.find_element_by_name("submit").click()
        time.sleep(2)
        content = self.driver.page_source
        time1 = re.findall(r'<tr bgcolor="#FFCC99">(.*?)</tr>', content, re.S)  # 匹配时间地区
        if time1 != []:
            time2 = time1[0] # 匹配时间地区
            time_clear = re.findall(r'<b>(.*?)</b>', time2, re.S)
            are_str = time_clear[1]        
            section_list = re.findall(r'(<tr.*?>.*?</tr>)',re.search(r'<table cellpadding="4" cellspacing="1">(.*?)</table>',content,re.S).group(),re.S)
            timedate = None
            for section in section_list[1:]:
                time_d = re.findall(r'<td.*?><b>(.*?)</b></td>',section,re.S)
                if time_d != []:
                    timedate = time_d[0]
                res_list = []
                aim_list = re.findall(r'<tr bgcolor="#CCCCCC">(.*?)</tr>', section, re.S)
                for aim in aim_list:
                    aim_clear = re.findall(r'<td.*?>(.*?)</td>', aim, re.S)
                    if "有名额" in aim_clear:
                        aim_clear[0] = timedate + are_str
                        self.aim_clear_api = aim_clear
                        res_list.append(aim_clear)
                with open("result.csv", "w") as csvfile:  # 保存到csv
                    writer = csv.writer(csvfile)
                    writer.writerows(res_list)
            return "secess"
        else:
            return content

    def start(self, month, are):
        error_time = str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
        # try:
        self.month(month)
        self.are(are)
        content = self.get_zuowei()
        if content != "secess":
            error_font_list = re.findall(r'<font.*?>(.*?)</font>', content, re.S) 
            if error_font_list:
                error_font = error_font_list[0]    # 处理出现弹框错误
                self.error_list.append(["%s"%month,"%s"%are])
                with open("error_chose.txt", "a") as f:
                    f.write("%s|%s|%s|%s\n" % (error_time, month, are, error_font))
            else: # 处理无法获得页面的错误（ip被封，进程被占）
                with open("%s%s.txt"%(month,are), "a") as f:
                    f.write(content)
                    self.error_list.append(["%s,%s"%(month,are)])
        # except Exception as e :
        # with open("error.txt", "a") as f:
        #     f.write("%s|%s|%s \n %s \n" % (error_time, month, are, e))
        #     self.error_list.append("%s"%are)

        # finally:
        self.driver.back()
        self.driver.refresh()

    def close(self):
        """关闭浏览器"""
        self.driver.quit()

    def run(self,month, are):
        self.open_url()
        while True:
            # 判断是否登陆成功
            judge = self.login()
            if judge:
                break
            else:
                continue
        self.search_zuowei()
        time.sleep(1)

        self.start(month, are)
        print self.error_list
        i = 0
        while self.error_list:
            error_message = self.error_list.pop()
            print error_message
            self.start(month, are)
            print self.error_list
            i += 1
            if i > 1:
                self.close()
                return "error"
        return self.aim_clear_api
        

# 定义函数，参数是函数的两个参数，都是python本身定义的，默认就行了。
# def application(environ, start_response):
#     # 定义文件请求的类型和当前请求成功的code
#     start_response('200 OK', [('Content-Type', 'text/html')])
#     # environ是当前请求的所有数据，包括Header和URL，body，这里只涉及到get
#     # 获取当前get请求的所有数据，返回是string类型
#     # params = parse_qs(environ['QUERY_STRING'])
#     # 获取get中key为name的值
#     # name = params.get('name', [''])[0]
#     # no = params.get('no', [''])[0]

#     # 组成一个数组，数组中只有一个字典

#     tuoful = Touful()
#     while True:
#         res = tuoful.run("201806","Beijing")
#         if res != "error":
#             print "完成抓取"
#             tuoful.close()
#             l = res
#             dic = {"q":{"time":"%s"%l[0],"sign":"%s"%l[1], "detail":"%s"%l[2], "money":"%s"%l[3], "zhuangtai":"%s"%l[4]}
    
# }

#             return [json.dumps(dic)]


#             break
    # time.sleep(30)
#     l = res
#     dic = {"q":{"time":"%s"%l[0],"sign":"%s"%l[1], "detail":"%s"%l[2], "money":"%s"%l[3], "zhuangtai":"%s"%l[4]}
    
# }

#     return [json.dumps(dic)]


# if __name__ == "__main__":
#     port = 5088
#     httpd = make_server("0.0.0.0", port, application)
#     print "serving http on port {0}...".format(str(port))
#     httpd.serve_forever()

if __name__ == '__main__':
    tuoful = Touful()
    while True:
        res = tuoful.run("201806","Beijing")
        if res == "secess":
            print "完成抓取"
            tuoful.close()
            break



