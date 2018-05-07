# encoding:utf-8
'''
author: ztcooper(github)
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
        p_province = re.compile(r'"法院省份":"(.*?)"')
        p_city = re.compile(r'"法院地市":"(.*?)"')
        p_area1 = re.compile(r'"法院区县":"(.*?)"')
        p_area2 = re.compile(r'"法院区域":"(.*?)"')

        self.item['title'] = p_title.findall(source)        # 标题
        self.item['pubdate'] = p_pubdate.findall(source)        # 发布时间
        self.item['region'] = p_province.findall(source)[0] + " " + p_city.findall(
            source)[0] + " " + (p_area1.findall(source)[0] or p_area2.findall(source)[0])    # 地区
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
