#! python3
# coding:utf-8
import requests,pdfkit
from bs4 import BeautifulSoup

def get_url_list():
    response = requests.get("http://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000")
    soup = BeautifulSoup(response.content, "html.parser")
    contents = soup.find_all(class_="ul.uk-nav.uk-nav-side")[1]
    urls=[]
    for url in contents.find_all("li"):
        url = "http://www.liaoxuefeng.com" + url.a.get("href")
        urls.append(url)
    return urls

def parse_url_html(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    body = soup.find_all(class_="x-wiki-content")[0]
    html = str(body)
    with open('a.html','wb') as f:
        f.write(html)

def save_pdf(htmls, file_name):
    options= {
        'page-size': 'Letter',
        'encoding': 'UTF-8',
        'custom-header': [
            ('Accept-Encoding', 'gzip')  # what is gzip?
    ]
    }
    pdfkit.from_file(htmls, file_name, options=options)

parse_url_html(get_url_list())
htmls = open('a.html', 'rb')
save_pdf(htmls, 'liaoxuefeng')
htmls.close()