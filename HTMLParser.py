# encoding:utf-8
'''
解析页面，得到数据
'''
from bs4 import BeautifulSoup
import re
import json


class HtmlParser(object):
    def __init__(self):
        self.item = dict()

    def parse(self, source):
        p = re.compile(r'jsonHtmlData =(.*?)}";')
        target = eval(json.loads(p.findall(source)[0] + '}"'))

        self.item['title'] = target['Title']		# 标题
        self.item['pubdate'] = target['PubDate']		# 发布时间
        html = target['Html']
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


def test():
	with open('test.txt') as f:
        source = f.read()
    s = HtmlParser()
    s.parse(source)
    print(s.item)

    
if __name__ == '__main__':
    test()
