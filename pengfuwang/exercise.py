#! python2
# coding:utf-8

import urllib, requests
import re
from bs4 import BeautifulSoup
import sys

# reload(sys) 教程写的，不知何用 todo
# sys.setdefaultencoding('utf-8')

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36'
    }

def get_html(index):
    url = 'https://www.pengfu.com/index_%d.html' % index
    html = requests.get(url, headers=headers).content
    # html = urllib.urlopen(url).read()
    return html

def get_blocks(html):
    soup = BeautifulSoup(html, "html.parser")
    blocks = soup.find_all(class_="list-item bg1 b1 boxshadow")
    return blocks

def get_title(block):
    h1 = block.find('h1')
    pattern = r'<h1 class="dp-b"><a href=".*?" target="_blank">(.*?)</a>'
    title = re.compile(pattern).findall(str(h1))
    return title

def get_pic(block):
    img = block.find_all('img')[1]
    gif_pattern = r'gifsrc="(.*?)"'
    jpg_pattern = r'<img .*? jpgsrc="(.*?)" src=".*?" .*?/>'
    # 如何用一条语句匹配 gif & jpg ? todo
    gif_pic = re.compile(gif_pattern).findall(str(img))
    jpg_pic = re.compile(jpg_pattern).findall(str(img))
    if gif_pic:
        return gif_pic
    else:
        return jpg_pic

def download(title, pic):
    if pic[-1] == 'g':
        path = 'img\%s.jpg' % title.decode('utf-8').encode('gbk')
    else:
        path = 'img\%s.gif' % title.decode('utf-8').encode('gbk')
    urllib.urlretrieve(pic, path)

def run(pagenum):
    for i in range(1,pagenum+1):
        html = get_html(i)
        blocks = get_blocks(html)
        for block in blocks:
            title = get_title(block)
            pic = get_pic(block)
            if pic:
                print 'downloading - ' + title[0]
                download(title[0], pic[0])
            else:
                continue

if __name__ == '__main__':
    run(1)
