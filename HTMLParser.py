# encoding:utf-8
'''
author: ztcooper
contact: 1060214139@qq.com
LICENSE: MIT

解析页面，得到数据
'''

from bs4 import BeautifulSoup
import re


class HtmlParser(object):
    def __init__(self):
        self.item = dict()

    def parse(self, source):
        p_title = re.compile(r'"Title\\":\\"(.*?)\\"')
        p_pubdate = re.compile(r'"PubDate\\":\\"(.*?)\\"')
        p_html = re.compile(r'"Html\\":\\"(.*?)\\"')

        self.item['title'] = p_title.findall(source)        # 标题
        self.item['pubdate'] = p_pubdate.findall(source)        # 发布时间
        html = p_html.findall(source)[0]
        # 提取正文
        soup = BeautifulSoup(html, 'lxml')
        divs = soup.find_all('div')
        article = ""
        for div in divs:
            try:
                article += div.get_text()
            except TypeError:
                continue
        self.item['article'] = article.strip()  # 正文
        return self.item
