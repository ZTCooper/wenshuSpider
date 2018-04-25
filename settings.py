# encoding:utf-8
'''
设置
'''


class Settings(object):
    def __init__(self):
        self.Param = "全文检索:*"  # 搜索关键字
        self.Index = 1  # 第几页
        self.Page = 20  # 每页几条
        self.Order = "法院层级"  # 排序标准
        self.Direction = "asc"  # asc正序 desc倒序

    def get_all(self):
        return self.Param, self.Index, self.Page, self.Order, self.Direction
