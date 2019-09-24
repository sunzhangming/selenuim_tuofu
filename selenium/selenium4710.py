# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
# 滚动函数
from selenium.webdriver.common.action_chains import ActionChains
# 代理函数
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.proxy import ProxyType
from selenium.webdriver.common.proxy import Proxy
from pymongo import *
import csv
import time
import re
# 接打码平台
from dama4710 import YDMHttp
import sys
reload(sys)
sys.setdefaultencoding('utf8')


class Touful(object):
    def __init__(self):
        # # 初始化浏览器
        # proxy = Proxy(
        #             {
        #             'proxyType': ProxyType.MANUAL,
        #             'httpProxy': '120.77.35.48:8899'  # 代理ip和端口
        #             }
        #             )
        # # 新建一个“期望技能”，哈哈
        # desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
        # # 把代理ip加入到技能中
        # proxy.add_to_capabilities(desired_capabilities)
        # self.driver = webdriver.PhantomJS(desired_capabilities=desired_capabilities)
        # self.driver = webdriver.PhantomJS()
        
        chrome_options = Options()
        # chrome_options.add_argument("--proxy-server=http://120.77.35.48:8899")
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        # self.driver.get("http://httpbin.org/ip")
        # print(self.driver.page_source)
        self.error_list = [] # 爬取失败的城市
        

        # 链接mongo
        # client = MongoClient('主机ip',端口)
        

    def open_url(self):
        """获取浏览器对象"""
        # get方法会一直等到页面被完全加载，然后才会继续程序，通常测试会在这里选择 time.sleep(2)
        self.driver.get("https://toefl.etest.net.cn/cn/")
        time.sleep(2)

    def login(self):
        """登录"""
        self.driver.find_element_by_id("id_username").clear()
        self.driver.find_element_by_id("id_pwd").clear()
        self.driver.find_element_by_id("id_username").send_keys(u"8398103")
        self.driver.find_element_by_id("id_pwd").send_keys(u"198476zwJ_A")
        self.driver.find_element_by_id("a_changeone").click()
        time.sleep(2)
        self.driver.save_screenshot("tuoful4710.png")  # 截取当前页面全图
        im = Image.open("tuoful4710.png")
        im = im.crop((232, 287, 322, 322))
        im.save("yz4710.png")
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
        self.driver.save_screenshot("tuoful4710.png")  # 截取当前页面全图
        im = Image.open("tuoful4710.png")
        im = im.crop((314, 478, 404, 513))
        im.save("yz4710.png")
        # codeContent2 = raw_input("读取验证码内容：")#临时
        codeContent2 = YDMHttp().start()
        self.driver.find_element_by_name("afCalcResult").send_keys(codeContent2)
        time.sleep(30)
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
                        res_list.append(aim_clear)
                with open("test4710.csv", "ab+") as csvfile:  # 保存到csv
                    writer = csv.writer(csvfile)
                    writer.writerows(res_list)
            return "no error"
        else:
            return content

    def start(self, month, are, month_list, are_list):
        error_time = str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
        try:
            self.month(month)
            self.are(are)
            content = self.get_zuowei()
            if content != "no error":
                error_font_list = re.findall(r'<font.*?>(.*?)</font>', content, re.S) 
                if error_font_list:
                    error_font = error_font_list[0]    # 处理出现弹框错误
                    with open("error.txt", "a") as f:
                        f.write("%s|%s|%s|%s\n" % (error_time, month, are, error_font))
                        self.error_list.append("%s"%are)
                    if "Please login first." in error_font:
                        month_index = month_list.index(month)
                        are_index = are_list.index(are)
                        if are_list[are_index] == are_list[-1]:
                            are_error_list = self.error_list
                        else:
                            are_error_list = self.error_list + are_list[are_index+1:]
                        month_error_list = month_list[month_index:]
                        res_relogin = [month_error_list, are_error_list]
                        error_relogin = Error()
                        error_relogin.month_xunhuan(res_relogin, are_list)
                else: # 处理无法获得页面的错误（ip被封，进程被占）
                    with open("%s%s.txt"%(month,are), "a") as f:
                        f.write(content)
                        self.error_list.append("%s"%are)
        except Exception as e :
            with open("error.txt", "a") as f:
                f.write("%s|%s|%s \n %s \n" % (error_time, month, are, e))
                self.error_list.append("%s"%are)

        finally:
            self.driver.back()
            self.driver.refresh()

    def close(self):
        """关闭浏览器"""
        self.driver.quit()

    def run(self,month_list,are_list):
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
        
        # are_list = ["Beijing", "Hebei", "Shanxi", "Tianjin", "Anhui", "Fujian"]
        for month in month_list:
            month_index = month_list.index(month)
            for are in are_list:
                self.start(month, are, month_list, are_list)
                print self.error_list
            i = 0
            while self.error_list:
                error_message = self.error_list.pop()
                print error_message
                self.start(month, error_message, month_list, are_list)
                print self.error_list
                if self.error_list:
                    if error_message == self.error_list[-1]: 
                        i = i+1
                        if i>1:
                            self.close()
                            return [month_list[month_index:], self.error_list]
        return [[], []]

        
                
class Error(object):
    """错误处理"""

    def month_xunhuan(self,res,are_list):
        """错误处理-月份断点"""
        global tuoful
        if res[1]:
            self.are_xunhuan(res)
        if len(res[0]) > 1:
            tuoful = Touful()
            res = tuoful.run(res[0][1:],are_list)
            return self.month_xunhuan(res,are_list)
        else:
            tuoful.close()
            return  False

    def are_xunhuan(self,res):
        """错误处理-地区断点"""
        global tuoful
        if res[1]:
            tuoful = Touful()
            res = tuoful.run([res[0][0]],res[1])
            return self.are_xunhuan(res)
        else:
            tuoful.close()
            return False

if __name__ == '__main__':
    tuoful = Touful()
    error = Error()
    # 日期变动
    month_list = []
    s = int(time.strftime('%Y%m',time.localtime(time.time())))-2
    m = int(time.strftime('%m',time.localtime(time.time())))-2
    while m<9:
        m = m+3
        s = s+3
        month_list.append(str(s))
    are_list = ["Beijing", "Hebei", "Shanxi", "Tianjin", "Anhui", "Fujian", "Jiangsu", "Jiangxi", "Shandong"
            , "Shanghai", "Zhejiang", "Guangdong", "Guangxi", "Guizhou", "Hainan", "Henan", "Hubei", "Hunan","Heilongjiang"
            , "Jilin", "Liaoning", "Gansu", "Inner Mongolia", "Ningxia", "Qinghai", "Shaanxi", "Xinjiang", "Chongqing"
            ,"Sichuan", "Tibet", "Yunnan"]
    # are_list = ["Beijing"]
    res = tuoful.run(month_list,are_list)
    error.month_xunhuan(res,are_list)
    
        
    



