# encoding:utf-8
'''
author: ztcooper
contact: 1060214139@qq.com
LICENSE: MIT

爬虫调度器（入口）
'''
from URLManager import UrlManager
from HTMLDownloader import HtmlDownloader
from HTMLParser import HtmlParser
from DataOutput import DataOutput
from settings import Settings
from random import random
import time
import threading
import multiprocessing


manager = UrlManager()
downloader = HtmlDownloader()
parser = HtmlParser()
db = DataOutput()  # 实例化时连接到数据库
db.create_table()      # 创建表
s = Settings().setting
old_total = db.get_total()
max_threads = 3
base_url = "http://wenshu.court.gov.cn/CreateContentJS/CreateContentJS.aspx?DocID="


# 逐条爬取
def crawl():
    old_total = db.get_total()
    while db.has_unvisited():
        docid = manager.get_one_docid(db)
        url = base_url + docid
        try:
            html = downloader.download(url)
            data = parser.parse(html)
            db.insert_into_db(data, docid)        # 插入数据库
        except Exception:
            db.change_status(docid, -1)
        time.sleep(random())
    new_total = db.get_total()
    db.close_cursor()
    print('新增', new_total - old_total, '条')


'''
    threads = []    # 线程队列
    while threads or db.has_unvisited():
        for thread in threads:
            if not thread.is_alive():   # 线程不可用
                threads.remove(thread)  # 从线程队列中删掉
        while len(threads) < max_threads and db.has_unvisited():
            thread = threading.Thread(target=run, args=(manager.get_one_docid(db),))    # 创建线程
            thread.setDaemon(True)  # 设置守护线程
            thread.start()  # 启动线程
            threads.append(thread)  # 加入线程队列
            time.sleep(random())
'''

# 将需要爬取的docid存入数据库
def store_ids():
    Page = s["Page"]
    for region in s["regions"]:
        for Order in s["Order"]:
            for Direction in s["Direction"]:
                Param = s["Param"] + region

                threads = []    # 线程队列
                Index = s["Index"][0]
                while threads or Index <= s["Index"][1]:
                    for thread in threads:
                        if not thread.is_alive():   # 线程不可用
                            threads.remove(thread)  # 从线程队列中删掉
                    while len(threads) < max_threads and Index <= s["Index"][1]:
                        thread = threading.Thread(
                            target=manager.store_docids, args=(Param, Index, Page, Order, Direction, db, ))    # 创建线程
                        thread.setDaemon(True)  # 设置守护线程
                        thread.start()  # 启动线程
                        threads.append(thread)  # 加入线程队列
                        time.sleep(random())
                        Index += 1


if __name__ == '__main__':
    print('获取url……')
    store_ids()
    print('开始爬取……')
    crawl()
