import json
from GetAPI import GetAPI


class UrlManager(object):
    def __init__(self):
        self.urls = set()

    def get_DocID(self):
        docids = []
        Param = "全文检索:*"  # 搜索关键字
        Index = 1  # 第几页
        Page = 20  # 每页几条
        Order = "法院层级"  # 排序标准
        Direction = "asc"  # asc正序 desc倒序
        data = GetAPI().get_data(Param, Index, Page, Order, Direction)
        for i in range(1, Page + 1):
            docids.append(eval(json.loads(data))[i]["文书ID"])
        return docids

    def add_new_urls(self):
        docids = self.get_DocID()
        for id in docids:
            self.urls.add(
                "http://wenshu.court.gov.cn/CreateContentJS/CreateContentJS.aspx?DocID=" + id)


if __name__ == '__main__':
    s = UrlManager()
    s.add_new_urls()
    print(s.urls)
