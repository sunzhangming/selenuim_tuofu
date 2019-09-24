# -*- coding: utf-8 -*-
from selenium import webdriver
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
from dama import YDMHttp
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
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_argument("--proxy-server=http://120.77.35.48:8899")
        self.driver = webdriver.Chrome(chrome_options=chromeOptions)
        self.driver.get("http://httpbin.org/ip")
        print(self.driver.page_source)
        self.error_list = [] # 爬取失败的城市
        # 日期变动
        self.month_list = []
        s = int(time.strftime('%Y%m',time.localtime(time.time())))-3
        m = int(time.strftime('%m',time.localtime(time.time())))-3
        while m<=9:
            m = m+3
            s = s+3
            self.month_list.append(str(s))

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
        self.driver.find_element_by_id("id_username").send_keys(u"1281490")
        self.driver.find_element_by_id("id_pwd").send_keys(u"Zengyichao!123")
        self.driver.find_element_by_id("a_changeone").click()
        time.sleep(2)
        self.driver.save_screenshot("tuoful.png")  # 截取当前页面全图
        element = self.driver.find_element_by_id("imgVerifycode")  # 验证码的按钮
        # 计算出元素上、下、左、右 位置
        left = element.location["x"]
        top = element.location["y"]
        right = element.location["x"] + element.size["width"]
        bottom = element.location["y"] + element.size["height"]
        im = Image.open("tuoful.png")
        im = im.crop((int(left), int(top), int(right), int(bottom)))
        im.save("yz.png")
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
        self.driver.save_screenshot("tuoful.png")  # 截取当前页面全图
        # element = self.driver.find_element_by_xpath('//*[@id="maincontent"]/form/table[3]//tr[2]/td[2]/table//tr/td[1]/img')  # 验证码的按钮
        # 计算出元素上、下、左、右 位置
        # left = element.location["x"]
        # top = element.location["y"]
        # right = element.location["x"] + element.size["width"]
        # bottom = element.location["y"] + element.size["height"]
        im = Image.open("tuoful.png")
        #im = im.crop((left, top, right, bottom))
        im = im.crop((314.0, 377.0, 404.0, 412.0))
        im.save("yz.png")
        # codeContent2 = raw_input("读取验证码内容：")#临时
        codeContent2 = YDMHttp().start()
        self.driver.find_element_by_name("afCalcResult").send_keys(codeContent2)
        self.driver.find_element_by_name("submit").click()
        time.sleep(2)
        content = self.driver.page_source
        time1 = re.findall(r'<tr bgcolor="#FFCC99">(.*?)</tr>', content, re.S)[0]  # 匹配时间地区
        time_clear = re.findall(r'<b>(.*?)</b>', time1, re.S)
        time_str = time_clear[0] + time_clear[1]
        res_list = []
        aim_list = re.findall(r'<tr bgcolor="#CCCCCC">(.*?)</tr>', content, re.S)
        for aim in aim_list:
            aim_clear = re.findall(r'<td.*?>(.*?)</td>', aim, re.S)
            if "有名额" in aim_clear:
                aim_clear[0] = time_str
                res_list.append(aim_clear)
        with open("test.csv", "ab+") as csvfile:  # 保存到csv
            writer = csv.writer(csvfile)
            # 先写入columns_name
            writer.writerow(
                ["time----------", "id----------", "dizhi--------------------------------------", "money----------",
                "zhuangtai---------"])
            # 写入多行用writerows
            writer.writerows(res_list)

    def start(self, month, are):
        try:
            self.month(month)
            # time.sleep(1)
            self.are(are)
            # time.sleep(1)
            self.get_zuowei()
            time.sleep(15)
        except:
            with open("error.txt", "a") as f:
                f.write("%s%s\n" % (month, are))
            self.error_list.append(["%s" % month, "%s" % are])
        finally:
            self.driver.back()
            self.driver.refresh()

    def close(self):
        """关闭浏览器"""
        self.driver.quit()

    def run(self):
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
        are_list = ["Beijing", "Hebei", "Shanxi", "Tianjin", "Anhui", "Fujian", "Jiangsu", "Jiangxi", "Shandong"
            , "Shanghai", "Zhejiang", "Guangdong", "Guangxi", "Guizhou", "Hainan", "Henan", "Hubei", "Hunan","Heilongjiang"
            , "Jilin", "Liaoning", "Gansu", "Inner Mongolia", "Ningxia", "Qinghai", "Shaanxi", "Xinjiang", "Chongqing"
            ,"Sichuan", "Tibet", "Yunnan"]
        for month in self.month_list:
            for are in are_list:
                self.start(month, are)
                print self.error_list
            while self.error_list:
                self.start(self.error_list[0][0], self.error_list[0][1])
                del self.error_list[0]
                print self.error_list


if __name__ == '__main__':
    tuoful = Touful()
    tuoful.run()
    tuoful.close()



