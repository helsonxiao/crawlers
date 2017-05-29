#! python3
# coding:utf-8
import requests
import time
from bs4 import BeautifulSoup
from http import cookiejar

session = requests.session()
# LWP - Light Weight Process
session.cookies = cookiejar.LWPCookieJar(filename='cookies.txt')
try:
    session.cookies.load(ignore_discard=True)
except:
    print('load cookies failed.')

def get_xsrf():
    res = requests.get('www.zhihu.com', headers=headers)
    soup = BeautifulSoup(res.content, 'html.parser')
    xsrf = soup.find('input', attrs={'name': '_xsrf'}).get('value')
    return xsrf

def get_captcha():
    """
    保存验证码图片至本地，人工识别
    :return:
    """