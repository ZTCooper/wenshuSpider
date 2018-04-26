# encoding:utf-8
'''
通过DocID构造接口链接
'''
# import json
import re
from GetAPI import GetAPI
from settings import Settings
from DataOutput import DataOutput


class UrlManager(object):
    def __init__(self):
        self.new_urls = set()  # 未爬取
        self.old_urls = set()  # 已爬取

    def get_DocID(self):
        docids = list()
        s = Settings()
        Param, Indexs, Page, Order, Direction = s.get_all()
        p_docid = re.compile(r'"文书ID\\":\\"(.*?)\\"')
        for Index in range(1, Indexs + 1):
            data = GetAPI().get_data(Param, Index, Page, Order, Direction)
            docids.extend(p_docid.findall(data))
        return docids

    def add_new_urls(self):
        db = DataOutput()
        old_docids = db.get_old_docids()
        db.close_cursor()
        docids = self.get_DocID()
        for docid in docids:
            if docid not in old_docids:     # 去重
                self.new_urls.add(
                    "http://wenshu.court.gov.cn/CreateContentJS/CreateContentJS.aspx?DocID=" + docid)

    def get_new_url(self):
        new_url = self.new_urls.pop()
        self.old_urls.add(new_url)
        return new_url

    def new_urls_size(self):
        return len(self.new_urls)

    def old_urls_size(self):
        return len(self.old_urls)


def test():
    s = UrlManager()
    s.add_new_urls()
    print(s.urls)


if __name__ == '__main__':
    test()
