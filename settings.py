# encoding:utf-8
'''
设置
'''


class Settings(object):
    def __init__(self):
        self.setting = {
            "Param": "全文检索:*",  # 搜索关键字
            "Index": [1, 3],  # 爬取页数
            "Page": 20,  # 每页几条
            "Order": "法院层级",  # 排序标准
            "Direction": "asc",  # asc正序 desc倒序
        }
