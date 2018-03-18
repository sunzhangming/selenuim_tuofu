# -*- coding: utf-8 -*-
# 导入 webdriver
from selenium import webdriver
import csv
import time
import re
import sys 
reload(sys) 
sys.setdefaultencoding('utf8')

def open_url():
    """获取浏览器对象"""
    driver = webdriver.Chrome()
    # get方法会一直等到页面被完全加载，然后才会继续程序，通常测试会在这里选择 time.sleep(2)
    driver.get("https://toefl.etest.net.cn/cn/")
    
    return driver

def login(driver):
    """登录"""
    driver.find_element_by_id("id_username").send_keys(u"1281490")
    driver.find_element_by_id("id_pwd").send_keys(u"Zengyichao!123")
    driver.find_element_by_id("a_changeone").click()
    codeContent = raw_input("读取验证码内容：")#临时
    driver.find_element_by_id("input_vcode").send_keys(codeContent)
    driver.find_element_by_id("id_login").click()
    
    return driver

def search_zuowei(driver):
    """查询空置考场"""
    driver.find_element_by_link_text("考位查询").click()
    
    return driver

def month(driver,month):
    """返回一个月份"""
    # checkboxs_month = driver.find_elements_by_xpath('//*[@id="mvfAdminMonths"]')
    # print len(checkboxs_month)
    # print checkboxs_month
    # g = (a.click() for a in checkboxs_month)
    driver.find_elements_by_xpath('//input[@value="%s"]'%month)[0].click()
    
    return driver

def are(driver,are):
    """返回一个地区"""
    # checkboxs_are = driver.find_elements_by_xpath('//*[@id="mvfSiteProvinces"]')
    # print len(checkboxs_are)
    # G = (b.click() for b in checkboxs_are)
    driver.find_elements_by_xpath('//input[@value="%s"]'%are)[0].click()
    
    return driver

def get_zuowei(driver):
    """得到一个月的一个地区的考场信息"""
    codeContent2 = raw_input("读取验证码内容：")#临时
    driver.find_element_by_name("afCalcResult").send_keys(codeContent2)
    driver.find_element_by_name("submit").click()
    content = driver.page_source
    time.sleep(3)
    time1 = re.findall(r'<tr bgcolor="#FFCC99">(.*?)</tr>',content,re.S)[0]#匹配时间地区
    time_clear = re.findall(r'<b>(.*?)</b>',time1,re.S)
    time_str = time_clear[0]+time_clear[1]
    aim_list = re.findall(r'<tr bgcolor="#CCCCCC">(.*?)</tr>',content,re.S)
    res_list = []
    for aim in aim_list:
        aim_clear = re.findall(r'<td.*?>(.*?)</td>',aim,re.S)
        if "有名额" in aim_clear:
            aim_clear[0] = time_str
            res_list.append(aim_clear)
    with open("test.csv","ab+") as csvfile: # 保存到csv
        writer = csv.writer(csvfile)
        #先写入columns_name
        writer.writerow(["time--这--","id--是--","dizhi--分--","money--割--","zhuangtai--线--"])
        #写入多行用writerows
        writer.writerows(res_list)
    
    return driver


def close(driver):
    """关闭浏览器"""
    driver.quit()

if __name__ == '__main__':
    driver = open_url()
    driver = login(driver)
    driver = search_zuowei(driver)
    try:
        driver = month(driver,"201803")
        time.sleep(1)
        driver = are(driver,"Beijing")
        time.sleep(1)
        driver = get_zuowei(driver)
        driver.back()
        driver.refresh()
        time.sleep(15)
    except Exception as e:
        with open("error.txt","a") as f:
            f.write("%s201803-Beijing\n"%e)
    try:
        driver = month(driver,"201803")
        time.sleep(1)
        driver = are(driver,"Hebei")
        time.sleep(1)
        driver = get_zuowei(driver)
        driver.back()
        driver.refresh()
        time.sleep(15)
    except Exception as e:
        with open("error.txt","a") as f:
            f.write("%s201803-Hebei\n"%e)
    try:
        driver = month(driver,"201803")
        time.sleep(1)
        driver = are(driver,"Shanxi")
        time.sleep(1)
        driver = get_zuowei(driver)
        driver.back()
        driver.refresh()
        time.sleep(15)
    except Exception as e:
        with open("error.txt","a") as f:
            f.write("%s201803-Shanxi\n"%e)
    try:
        driver = month(driver,"201803")
        time.sleep(1)
        driver = are(driver,"Tianjin")
        time.sleep(1)
        driver = get_zuowei(driver)
        driver.back()
        driver.refresh()
        time.sleep(15)
    except Exception as e:
        with open("error.txt","a") as f:
            f.write("201803-Tianjin\n")
    try:
        driver = month(driver,"201803")
        time.sleep(1)
        driver = are(driver,"Anhui")
        time.sleep(1)
        driver = get_zuowei(driver)
        driver.back()
        driver.refresh()
        time.sleep(15)
    except:
        with open("error.txt","a") as f:
            f.write("201803-Anhui\n")
    try:
        driver = month(driver,"201803")
        time.sleep(1)
        driver = are(driver,"Fujian")
        time.sleep(1)
        driver = get_zuowei(driver)
        driver.back()
        driver.refresh()
        time.sleep(15)
    except:
        with open("error.txt","a") as f:
            f.write("201803-Fujian\n")
    try:
        driver = month(driver,"201803")
        time.sleep(1)
        driver = are(driver,"Jiangsu")
        time.sleep(1)
        driver = get_zuowei(driver)
        driver.back()
        driver.refresh()
        time.sleep(15)
    except:
        with open("error.txt","a") as f:
            f.write("201803-Jiangsu\n")
    try:
        driver = month(driver,"201803")
        time.sleep(1)
        driver = are(driver,"Jiangxi")
        time.sleep(1)
        driver = get_zuowei(driver)
        driver.back()
        driver.refresh()
        time.sleep(15)
    except:
        with open("error.txt","a") as f:
            f.write("201803-Jiangxi\n")
    try:
        driver = month(driver,"201803")
        time.sleep(1)
        driver = are(driver,"Shandong")
        time.sleep(1)
        driver = get_zuowei(driver)
        driver.back()
        driver.refresh()
        time.sleep(15)
    except:
        with open("error.txt","a") as f:
            f.write("201803-Shandong\n")
    try:
        driver = month(driver,"201803")
        time.sleep(1)
        driver = are(driver,"Shanghai")
        time.sleep(1)
        driver = get_zuowei(driver)
        driver.back()
        driver.refresh()
        time.sleep(15)
    except:
        with open("error.txt","a") as f:
            f.write("201803-Shanghai\n")
    try:
        driver = month(driver,"201803")
        time.sleep(1)
        driver = are(driver,"Zhejiang")
        time.sleep(1)
        driver = get_zuowei(driver)
        driver.back()
        driver.refresh()
        time.sleep(15)
    except:
        with open("error.txt","a") as f:
            f.write("201803-Zhejiang\n")
    try:
        driver = month(driver,"201803")
        time.sleep(1)
        driver = are(driver,"Guangdong")
        time.sleep(1)
        driver = get_zuowei(driver)
        driver.back()
        driver.refresh()
        time.sleep(15)
    except:
        with open("error.txt","a") as f:
            f.write("201803-Guangdong\n")
    try:
        driver = month(driver,"201803")
        time.sleep(1)
        driver = are(driver,"Guangxi")
        time.sleep(1)
        driver = get_zuowei(driver)
        driver.back()
        driver.refresh()
        time.sleep(15)
    except:
        with open("error.txt","a") as f:
            f.write("201803-Guangxi\n")
    try:
        driver = month(driver,"201803")
        time.sleep(1)
        driver = are(driver,"Guizhou")
        time.sleep(1)
        driver = get_zuowei(driver)
        driver.back()
        driver.refresh()
        time.sleep(15)
    except:
        with open("error.txt","a") as f:
            f.write("201803-Guizhou\n")
    try:
        driver = month(driver,"201803")
        time.sleep(1)
        driver = are(driver,"Hainan")
        time.sleep(1)
        driver = get_zuowei(driver)
        driver.back()
        driver.refresh()
        time.sleep(15)
    except:
        with open("error.txt","a") as f:
            f.write("201803-Hainan\n")
    try:
        driver = month(driver,"201803")
        time.sleep(1)
        driver = are(driver,"Henan")
        time.sleep(1)
        driver = get_zuowei(driver)
        driver.back()
        driver.refresh()
        time.sleep(15)
    except:
        with open("error.txt","a") as f:
            f.write("201803-Henan\n")
    try:
        driver = month(driver,"201803")
        time.sleep(1)
        driver = are(driver,"Hubei")
        time.sleep(1)
        driver = get_zuowei(driver)
        driver.back()
        driver.refresh()
        time.sleep(15)
    except:
        with open("error.txt","a") as f:
            f.write("201803-Hubei\n")
    try:
        driver = month(driver,"201803")
        time.sleep(1)
        driver = are(driver,"Hunan")
        time.sleep(1)
        driver = get_zuowei(driver)
        driver.back()
        driver.refresh()
        time.sleep(15)
    except:
        with open("error.txt","a") as f:
            f.write("201803-Hunan\n")
    try:
        driver = month(driver,"201803")
        time.sleep(1)
        driver = are(driver,"Heilongjiang")
        time.sleep(1)
        driver = get_zuowei(driver)
        driver.back()
        driver.refresh()
        time.sleep(15)
    except:
        with open("error.txt","a") as f:
            f.write("201803-Heilongjiang\n")
    try:
        driver = month(driver,"201803")
        time.sleep(1)
        driver = are(driver,"Jilin")
        time.sleep(1)
        driver = get_zuowei(driver)
        driver.back()
        driver.refresh()
        time.sleep(15)
    except:
        with open("error.txt","a") as f:
            f.write("201803-Jilin\n")
    try:
        driver = month(driver,"201803")
        time.sleep(1)
        driver = are(driver,"Liaoning")
        time.sleep(1)
        driver = get_zuowei(driver)
        driver.back()
        driver.refresh()
        time.sleep(15)
    except:
        with open("error.txt","a") as f:
            f.write("201803-Liaoning\n")
    try:
        driver = month(driver,"201803")
        time.sleep(1)
        driver = are(driver,"Gansu")
        time.sleep(1)
        driver = get_zuowei(driver)
        driver.back()
        driver.refresh()
        time.sleep(15)
    except:
        with open("error.txt","a") as f:
            f.write("201803-Gansu\n")
    try:
        driver = month(driver,"201803")
        time.sleep(1)
        driver = are(driver,"Neimenggu")
        time.sleep(1)
        driver = get_zuowei(driver)
        driver.back()
        driver.refresh()
        time.sleep(15)
    except:
        with open("error.txt","a") as f:
            f.write("201803-Neimenggu\n")
    try:
        driver = month(driver,"201803")
        time.sleep(1)
        driver = are(driver,"Ningxia")
        time.sleep(1)
        driver = get_zuowei(driver)
        driver.back()
        driver.refresh()
        time.sleep(15)
    except:
        with open("error.txt","a") as f:
            f.write("201803-Ningxia\n")
    try:
        driver = month(driver,"201803")
        time.sleep(1)
        driver = are(driver,"Shaanxi")
        time.sleep(1)
        driver = get_zuowei(driver)
        driver.back()
        driver.refresh()
        time.sleep(15)
    except:
        with open("error.txt","a") as f:
            f.write("201803-Shaanxi\n")
    try:
        driver = month(driver,"201803")
        time.sleep(1)
        driver = are(driver,"Xinjiang")
        time.sleep(1)
        driver = get_zuowei(driver)
        driver.back()
        driver.refresh()
        time.sleep(15)
    except:
        with open("error.txt","a") as f:
            f.write("201803-Xinjiang\n")
    try:
        driver = month(driver,"201803")
        time.sleep(1)
        driver = are(driver,"Chongqing")
        time.sleep(1)
        driver = get_zuowei(driver)
        driver.back()
        driver.refresh()
        time.sleep(15)
    except:
        with open("error.txt","a") as f:
            f.write("201803-Chongqing\n")
    try:
        driver = month(driver,"201803")
        time.sleep(1)
        driver = are(driver,"Sichuan")
        time.sleep(1)
        driver = get_zuowei(driver)
        driver.back()
        driver.refresh()
        time.sleep(15)
    except:
        with open("error.txt","a") as f:
            f.write("201803-Sichuan\n")
    try:
        driver = month(driver,"201803")
        time.sleep(1)
        driver = are(driver,"Xizang")
        time.sleep(1)
        driver = get_zuowei(driver)
        driver.back()
        driver.refresh()
        time.sleep(15)
    except:
        with open("error.txt","a") as f:
            f.write("201803-Xizang\n")


        # with open("test.txt","w") as f:
        #   f.write(driver.page_source)
        #   # 关闭浏览器
        #   driver.quit()
        
    #   driver.save_screenshot("1.png")
    #   # 鼠标移动到 ac 位置
    #   ac = driver.find_element_by_xpath('//*[@id="footer"]/p[1]')
    #   time.sleep(2)
    #   ActionChains(driver).move_to_element(ac).perform()
    #   driver.save_screenshot("2.png")
    # 
