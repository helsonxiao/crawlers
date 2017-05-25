#! python3
# coding:utf-8
import requests,pdfkit,os,time
from bs4 import BeautifulSoup

def parse_url_html(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    body = soup.find_all(class_="x-wiki-content")[0]
    html = str(body)
    html = html.encode("utf-8")
    return html

def get_url_list():
    response = requests.get("http://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000")
    soup = BeautifulSoup(response.content, "html.parser")
    contents = soup.find_all(class_="uk-nav uk-nav-side")[1]
    urls=[]
    for url in contents.find_all("li"):
        url = "http://www.liaoxuefeng.com" + url.a.get("href")
        urls.append(url)
    return urls

def save_pdf(htmls):
    options= {
        'page-size': 'Letter',
        'encoding': 'UTF-8',
        'custom-header': [
            ('Accept-Encoding', 'gzip')
    ]
    }
    start_time = time.time()
    print(str(start_time))
    pdfkit.from_file(htmls, "liao.pdf", options=options)

urls = get_url_list()
htmls = []
for index, url in enumerate(urls):
    h_name = 'NO.%d.html' %index
    print("Please wait for crawler's work...")
    html = parse_url_html(url)
    with open(h_name, 'wb') as f:
        f.write(html)
    htmls.append(h_name)

save_pdf(htmls)
for html in htmls:
    os.remove(html)