import time 
# s = int(time.strftime('%Y%m',time.localtime(time.time())))
# m = int(time.strftime('%m',time.localtime(time.time())))
# while m<=10:
#     m = m+2
#     s = s+2
#     print s

s = int(time.strftime('%Y%m',time.localtime(time.time())))-1
m = int(time.strftime('%m',time.localtime(time.time())))-1
while m<=9:
    m = m+3
    s = s+3
    print s

# t = [1,2,3,4,5,6]
# h = t.index(2)
# print h,t[h:]
# def run(res):
#     res.pop()
#     print res
#     if res:
#         return res
#     else:
#         return []
    

# def xunhuan(res):
#     res = run(res)
#     if res:
#         xunhuan(res)
#     else:
#         return  []

# if __name__ == '__main__':
#     res = [1,2,4]
#     xunhuan(res)

class T(object):
    def j(self):
        y()

def y():
    print "f"

t = T()
t.j()