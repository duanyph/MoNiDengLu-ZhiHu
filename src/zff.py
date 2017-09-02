'''
Created on 2017年8月31日

@author: duany
'''
import requests
import http.cookiejar
import re
import time
#获取_xsrf值
def hq_xsrf():
    global html1
    dk=hhbc.get("https://www.zhihu.com",headers=tou)
    html1=dk.text
    zz=r'name="_xsrf" value="(.*?)"'
    _xsrf=re.findall(zz,html1)
    return _xsrf[0]
#获取验证码
def yzm():
    sj = str(int(time.time() * 1000))
    url="https://www.zhihu.com/captcha.gif?r="+sj+"&type=login&lang=cn"
    hqyzm=hhbc.get(url,headers=tou)
    with open('yzm.gif', 'wb') as yzmtp:
        yzmtp.write(hqyzm.content)
        yzmtp.close()
    sryzm = input("请输入验证值>")
    return sryzm
html1=None
#构建头，会话，cookie等
tou={"Host": "www.zhihu.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0",
    "Accept": "*/*",
    "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://www.zhihu.com/",
    "Connection": "keep-alive",}
hhbc=requests.session()
hhbc.cookies=http.cookiejar.LWPCookieJar("cookie1")
try:
    hhbc.cookies.load( ignore_discard=True)
except:
    print("cookies未加载！")
#模拟登录
def dl():
    url="https://www.zhihu.com/login/email"
    sj={"_xsrf":hq_xsrf(),
        "password":"密码",
        "email":"账号",
        "captcha_type":"cn",
    }
    dl=hhbc.post(url, data=sj, headers=tou)
    dldm=dl.text
    #判断是否二维码登录
    if re.findall(r'"r": 1',dldm):
        zz=r'class="Captcha-prompt">(.*?)</'
        yzfs=re.findall(zz,html1)
        print(yzfs[0])
        yzm=yzm()
        sj["captcha"]=r'{"img_size":[200,44],"input_points":['+yzm+']}'
        dl=hhbc.post(url, data=sj, headers=tou)
    hhbc.cookies.save()
    pddl2=hhbc.get("https://www.zhihu.com/settings/profile",headers=tou,allow_redirects=False).status_code
    if pddl2==200:
        print("登录成功！")
    elif pddl==302:
        print("登录失败，请检查用户名密码及验证码是否正确！")
    else:
        print("出现错误，状态码："+pddl2)
pddl=hhbc.get("https://www.zhihu.com/settings/profile",headers=tou,allow_redirects=False).status_code
if pddl==200:
    print("登录成功！")
elif pddl==302:
    print("登录中！")
    dl()
else:
    print("错误！状态码："+pddl)
