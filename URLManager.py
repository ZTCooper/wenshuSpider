# encoding:utf-8
'''
通过DocID构造接口链接
'''
import json
from GetAPI import GetAPI
from settings import Settings


class UrlManager(object):
    def __init__(self):
        self.new_urls = set()  # 未爬取
        self.old_urls = set()  # 已爬取

    def get_DocID(self):
        docids = list()
        s = Settings()
        Param, Index, Page, Order, Direction = s.get_all()
        data = GetAPI().get_data(Param, Index, Page, Order, Direction)
        for i in range(1, Page + 1):
            docids.append(eval(json.loads(data))[i]["文书ID"])
        return docids

    def add_new_urls(self):
        docids = self.get_DocID()
        for id in docids:
            self.new_urls.add(
                "http://wenshu.court.gov.cn/CreateContentJS/CreateContentJS.aspx?DocID=" + id)

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
