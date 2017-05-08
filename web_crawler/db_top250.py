#! python2
# coding: utf-8

"""
爬取豆瓣top250 - 电影名
"""

import requests
import codecs
from bs4 import BeautifulSoup

DOWNLOAD_URL = "https://movie.douban.com/top250"


def download_page(url):
    # 添加 U-A 信息，以防反爬
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
    }
    data = requests.get(url, headers=headers).content
    return data


def parse_html(html):
    soup = BeautifulSoup(html)
    movie_list_soup = soup.find('ol', attrs={'class': 'grid_view'})

    movie_name_list = []

    for movie_list in movie_list_soup.find_all('li'):
        detail = movie_list.find('div', attrs={'class': 'hd'})
        movie_name = detail.find('span', attrs={'class': 'title'}).getText()

        movie_name_list.append(movie_name)

    next_page = soup.find('span', attrs={'class': 'next'}).find('a')  # 链式函数
    if next_page:
        return movie_name_list, DOWNLOAD_URL + next_page['href']
    else:
        return movie_name_list, None  # 到了最后一页返回None


def main():
    url = DOWNLOAD_URL  # 初始地址

    with codecs.open('movies', 'wb', encoding='utf-8') as fp:
        while url:  # 当url有意义时
            html = download_page(url)
            movies, url = parse_html(html)
            fp.write(u'{movies}\n'.format(movies='\n'.join(movies)))  # 给列表项们添加换行符

# 检测命名空间
if __name__ == '__main__':
    main()