# encoding:utf-8
'''
author: ztcooper(github)
contact: 1060214139@qq.com
LICENSE: MIT

通过DocID构造接口链接
'''

import re
from GetAPI import GetAPI
from DataOutput import DataOutput
import threading


class UrlManager(object):
    def __init__(self):
        # self.docids = set()
        self.lock = threading.Lock()      # 线程锁

    def get_DocID(self, Param, Index, Page, Order, Direction):
        p_docid = re.compile(r'"文书ID\\":\\"(.*?)\\"')
        data = GetAPI().get_data(Param, Index, Page, Order, Direction)
        return p_docid.findall(data)

    def store_docids(self, Param, Index, Page, Order, Direction, db):
        docids = self.get_DocID(Param, Index, Page, Order, Direction)
        region = Param.split(':')[1]    # 地域
        self.lock.acquire()     # 线程锁
        for docid in docids:
            if not db.in_error_list(docid):  # 不在异常队列中
                db.insert_docid(docid, region)      # docid存入数据库
        self.lock.release()

    def get_one_docid(self, db):
        if db.cur.execute('SELECT docid FROM info WHERE status = 0'):   # 未访问id
            docid = db.cur.fetchone()[0]
        elif db.cur.execute('SELECT docid FROM info WHERE status = -1'):    # 异常id
            docid = db.cur.fetchone()[0]
        elif db.cur.execute('SELECT docid FROM info WHERE status = 2'):    # 异常id
            docid = db.cur.fetchone()[0]
        if docid:
            db.change_status(docid, 2)      # 更改状态为正在访问
            return docid
        return None

    '''
    def get_urls(self):
        docids = self.docids.copy()     # 浅拷贝
        self.docids.clear()   # 每次urls中只存放一个列表页的url，减少开销
        return docids
    '''
