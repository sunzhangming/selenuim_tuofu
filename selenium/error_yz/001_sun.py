
# coding:utf-8

# from lxml import etree
import re
import csv
with open('hh.html','r') as f:
    content = f.read()


    # html = etree.HTML(b)
    # h = re.findall(r'<tr bgcolor="#E0E0E0">(.*?)<tr bgcolor="#E0E0E0">',b,re.S)
    # for t in h:
    #     print t
    #     reg=re.compile(r"<b>(.*?)</b>")
    #     match=reg.search(t)
    #     print match.group(0)
    #     c = re.findall(r'<tr bgcolor="#CCCCCC">(.*?)</tr>',t,re.S)
    #     for d in c:
    #         e = re.findall(r'<td.*?>(.*?)</td>',d,re.S)
    #         print(e)

    time1 = re.findall(r'<tr bgcolor="#FFCC99">(.*?)</tr>', content, re.S)[0]  # 匹配时间地区
    time_clear = re.findall(r'<b>(.*?)</b>', time1, re.S)
    time_str = time_clear[0] + time_clear[1]

    section_list = re.findall(r'(<tr.*?>.*?</tr>)',re.search(r'<table cellpadding="4" cellspacing="1">(.*?)</table>',content,re.S).group(),re.S)
    # res_list = []
    # print(section_list)
    timedate = None
    for section in section_list[1:]:
        with open("jj.html","a") as f:
            f.write(str(section_list))
        # reg=re.search(r"<b>(.*?)</b>",section)
        # print(section)
        # match=reg.search(section)
        # time_detail = match.group(0)
        # aim_list = re.findall(r'<tr bgcolor="#CCCCCC">(.*?)</tr>', section, re.S)
        time = re.findall(r'<td.*?><b>(.*?)</b></td>',section,re.S)
        if time != []:
            timedate = time[0]
        else:
        # for aim in aim_list:
            aim_clear = re.findall(r'<td.*?>(.*?)</td>', section, re.S)
            aim_clear[0] = timedate
            print(aim_clear)
        #     if "有名额" in aim_clear:
        #         aim_clear[0] = time_str+time_detail
        #         res_list.append(aim_clear)
        # with open("test.csv", "ab+") as csvfile:  # 保存到csv
        #     writer = csv.writer(csvfile)
        #     # 先写入columns_name
        #     writer.writerow(
        #         ["time----------", "id----------", "dizhi--------------------------------------", "money----------",
        #         "zhuangtai---------"])
        #     # 写入多行用writerows
        #     writer.writerows(res_list)