#! python3
# coding:utf-8

from __future__ import unicode_literals  # todo
import logging
import os
import re
import time

# https://docs.python.org/3/library/urllib.parse.html
from urllib.parse import urlparse  # py3

# https://pypi.python.org/pypi/pdfkit
import pdfkit
import requests
from bs4 import BeautifulSoup

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
</head>
<body>
{content}
</body>
</html>
"""

class Crawler(object):
    """
    爬虫父类/基类
    """
    name = None

    def __init__(self, name, start_url):
        """
        初始化
        :param name: 保存的 pdf 文件名，无需后缀 
        :param start_url: 爬虫入口 url
        """
        self.name = name
        self.start_url = start_url
        # 解析 url 并且生成域名
        self.domain = '{u.scheme}://{u.netloc}'.format(u=urlparse(self.start_url))

    def crawl(self, url):
        print("努力爬取中...")
        response = requests.get(url)
        return response

    def parse_menu(self, response):
        """
        解析目录结构，获取所有的URL，生成列表。由子类实现。
        :param response: 爬虫返回的 response 对象
        :return: url 可迭代对象(iterable)
        """
        raise NotImplementedError

    def parse_body(self, response):
        """
        解析正文。由子类实现。
        :param response: 爬虫返回的 response 对象
        :return: 返回经过处理的 HTML 文本
        """
        # In user defined base classes,
        # abstract methods should raise this exception when they require derived classes to override the method,
        # or while the class is being developed to indicate that the real implementation still needs to be added.
        raise NotImplementedError

    def run(self):
        start = time.time()
        options = {
            'page-size': 'Letter',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "UTF-8",
            'custom-header': [
                ('Accept-Encoding', 'gzip')  # gzip - A compression format
            ],
            'cookie': [
                ('cookie-name1', 'cookie-value1'),
                ('cookie-name2', 'cookie-value2'),
            ],
            'outline-depth': 10,
        }
        htmls = []
        for index, url in enumerate(self.parse_menu(self.crawl(self.start_url))):
            html = self.parse_body(self.crawl(url))
            f_name = ".".join([str(index), "html"])
            with open(f_name, "wb") as f:
                f.write(html)
            htmls.append(f_name)

        try:
            pdfkit.from_file(htmls, self.name + ".pdf", options=options)
        except:
            pass
        finally:
            for f_name in htmls:
                os.remove(f_name)
            total_time = time.time() - start
            print("总共耗时：{:f}".format(total_time))

class LiaoxuefengPythonCrawler(Crawler):
    """
    廖雪峰Python3教程
    """

    def parse_menu(self, response):
        """
        解析目录结构,获取所有URL目录列表
        :param response 爬虫返回的response对象
        :return: url生成器
        """
        soup = BeautifulSoup(response.content, "html.parser")
        menu_tag = soup.find_all(class_="uk-nav uk-nav-side")[1]
        for li in menu_tag.find_all("li"):
            url = li.a.get("href")
            if not url.startswith("http"):
                url = "".join([self.domain, url])  # 补全 url
            yield url  # generator - 惰性运行

    def parse_body(self, response):
        """
        解析正文
        :param response: 爬虫返回的response对象
        :return: 返回处理后的html文本
        """
        try:
            soup = BeautifulSoup(response.content, 'html.parser')
            body = soup.find_all(class_="x-wiki-content")[0]

            # 加入标题, 居中显示
            title = soup.find('h4').get_text()
            center_tag = soup.new_tag("center")
            title_tag = soup.new_tag('h1')
            title_tag.string = title
            center_tag.insert(1, title_tag)
            body.insert(1, center_tag)

            html = str(body)
            # body中的img标签的src相对路径的改成绝对路径
            pattern = "(<img .*?src=\")(.*?)(\")"  # 正则表达式分为 4 部分 - 0 完全匹配，123 分别对应括号内容

            # 将匹配到的内容 group 重组格式
            def func(ht):
                if not ht.group(2).startswith("http"):  # 无绝对路径则添加域名
                    full_url = "".join([ht.group(1), self.domain, ht.group(2), ht.group(3)])
                    return full_url
                else:
                    return ht.group(0)  # 有绝对路径则返回自身
                    # return "".join([ht.group(1), ht.group(2), ht.group(3)])

            html = re.compile(pattern).sub(func, html)  # 将 正则表达式 编译成 pattern 对象
            html = html_template.format(content=html)
            html = html.encode("utf-8")
            return html
        except Exception as e:
            logging.error("解析错误", exc_info=True)


if __name__ == '__main__':
    # start_url = "http://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000"
    start_url = "http://www.liaoxuefeng.com/wiki/0013739516305929606dd18361248578c67b8067c8c017b000"
    crawler = LiaoxuefengPythonCrawler("廖雪峰Git", start_url)
    crawler.run()
