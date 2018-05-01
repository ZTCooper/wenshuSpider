# encoding:utf-8
'''
author: ztcooper
contact: 1060214139@qq.com
LICENSE: MIT

通过DocID构造接口链接
'''
# import json
import re
from GetAPI import GetAPI
from DataOutput import DataOutput


class UrlManager(object):
    def __init__(self):
        self.urls = set()  # 未爬取
        # self.old_urls = set()  # 已爬取

    def get_DocID(self, Index):
        p_docid = re.compile(r'"文书ID\\":\\"(.*?)\\"')
        print("获取url中……")
        data = GetAPI().get_data(Index)
        return p_docid.findall(data)

    def add_urls(self, Index, db):
        docids = self.get_DocID(Index)
        duplicates = 0
        for docid in docids:
            if not db.check_duplicates(docid):     # 查重
                self.urls.add(
                    "http://wenshu.court.gov.cn/CreateContentJS/CreateContentJS.aspx?DocID=" + docid)
            else:
                duplicates += 1
        print("url构造完成，准备开始爬取……")
        return duplicates

    def get_urls(self):
        urls = self.urls.copy()     # 浅拷贝
        self.urls.clear()
        return urls


'''
    def urls_size(self):
        return len(self.urls)

    def old_urls_size(self):
        return len(self.old_urls)
'''

'''
def test():
    s = UrlManager()
    s.add_new_urls()
    print(s.urls)


if __name__ == '__main__':
    test()
'''
