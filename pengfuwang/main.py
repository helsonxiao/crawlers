# coding:utf-8

import urllib, requests, re
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


url = r'https://www.pengfu.com/'
html = urllib.urlopen(url).read()

def get_title_list():
    p = r'<h1 class=".*?"><a href=".*?" target="_blank">(.*?)</a>'
    pattern = re.compile(p)
    titles = re.findall(pattern, html)
    return titles

def get_content_list():
    p = r'<img src="(.*?)".*?>'
    pattern = re.compile(p)
    pics = re.findall(pattern,html)
    return pics

def download(tt, ct):
    path = 'img\%s.jpg' % tt.decode('utf-8').encode('gbk')
    urllib.urlretrieve(ct, path)

title_list = get_title_list()
content_list = get_content_list()
# print title_list
# print content_list

for title, content in zip(title_list, content_list):
    download(title, content)
    print title,content