# coding:utf-8

import urllib, requests, re
import sys

# reload(sys) 教程写的，不知何用 todo
# sys.setdefaultencoding('utf-8')

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36'
    }

def get_html(index):
    url = r'https://www.pengfu.com/index_%d.html' % index
    html = requests.get(url, headers=headers).content
    # html = urllib.urlopen(url).read()
    return html

def get_titles(html):
    pattern = r'<h1 class="dp-b"><a href=".*?" target="_blank">(.*?)</a>'
    titles = re.findall(pattern, html)
    return titles

def get_pics(html):
    pattern = r'<img src=".*?" width=".*?" height=".*?" .*?src="(.*?)">'
    pics = re.findall(pattern, html)
    return pics

def download(title, pic):
    if pic[-1] == 'g':
        path = 'img\%s.jpg' % title.decode('utf-8').encode('gbk')
    else:
        path = 'img\%s.gif' % title.decode('utf-8').encode('gbk')
    urllib.urlretrieve(pic, path)

def run(pagenum):
    for i in range(1,pagenum+1):
        html = get_html(i)
        titles = get_titles(html)
        pics = get_pics(html)

        for title, pic in zip(titles, pics):
            if pic:
                print title,pic
            else:
                continue
            download(title, pic)

run(2)
