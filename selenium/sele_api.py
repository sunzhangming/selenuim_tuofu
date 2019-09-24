# coding:utf-8

import json
from urlparse import parse_qs
from wsgiref.simple_server import make_server


# 定义函数，参数是函数的两个参数，都是python本身定义的，默认就行了。
def application(environ, start_response):
    # 定义文件请求的类型和当前请求成功的code
    start_response('200 OK', [('Content-Type', 'text/html')])
    # environ是当前请求的所有数据，包括Header和URL，body，这里只涉及到get
    # 获取当前get请求的所有数据，返回是string类型
    # params = parse_qs(environ['QUERY_STRING'])
    # 获取get中key为name的值
    # name = params.get('name', [''])[0]
    # no = params.get('no', [''])[0]

    # 组成一个数组，数组中只有一个字典
    
    l = ["2018年4月21日 09:00","河北","STN80053C","石家庄信息工程职业学院","1761","有名额"]
    k = ["2018年4月21日 09:00","河北","STN80053D","石家庄信息工程职业学院","1761","有名额"]
    m = ["2018年4月21日 09:00","山东","STN80094A","临沂大学","1761","有名额"]

    dic = {"q":{"time":"%s"%l[0], "are":"%s"%l[1],"sign":"%s"%l[2], "detail":"%s"%l[3], "money":"%s"%l[4], "zhuangtai":"%s"%l[5]}
    ,"w":{"time":"%s"%k[0], "are":"%s"%k[1],"sign":"%s"%k[2], "detail":"%s"%k[3], "money":"%s"%k[4], "zhuangtai":"%s"%k[5]}
    ,"e":{"time":"%s"%m[0], "are":"%s"%m[1],"sign":"%s"%m[2], "detail":"%s"%m[3], "money":"%s"%m[4], "zhuangtai":"%s"%m[5]}
}

    return [json.dumps(dic)]


if __name__ == "__main__":
    port = 5088
    httpd = make_server("0.0.0.0", port, application)
    print "serving http on port {0}...".format(str(port))
    httpd.serve_forever()