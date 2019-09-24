# coding:utf-8
from time import sleep
from PIL import Image
from selenium import webdriver
driver = webdriver.Chrome()
driver.get("https://toefl.etest.net.cn/cn/")
sleep(2)
driver.find_element_by_id("a_changeone").click()
driver.save_screenshot("tuoful.png")  # 截取当前页面全图
element = driver.find_element_by_id("imgVerifycode")  # 验证码的按钮
print "获取元素坐标："
location = element.location
print location

print "获取元素大小："
size = element.size
print size

# 计算出元素上、下、左、右 位置
left = element.location["x"]
top = element.location["y"]
right = element.location["x"] + element.size["width"]
bottom = element.location["y"] + element.size["height"]
print left,top,right,bottom
im = Image.open("tuoful.png")
im = im.crop((left, top, right, bottom))
im.save("yz.png")