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
import pyprind
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
lock = threading.Lock()
base_url = "http://wenshu.court.gov.cn/CreateContentJS/CreateContentJS.aspx?DocID="


def crawl():
    old_total = db.get_total()
    def run(Index):
        # 一个列表页的url存入数据库(默认为status为0)并加入urls set
        lock.acquire()
        manager.store_docids(Index, db)
        docids = manager.get_urls()
        for docid in docids:
            url = base_url + docid
            try:
                html = downloader.download(url)
                data = parser.parse(html)
                db.insert_into_db(data, docid)        # 插入数据库
            except TimeoutError:
                db.change_status(docid, -1)
        lock.release()
        new_total = db.get_total()
        print("新增", new_total - old_total, "条")
        old_total = new_total

    threads = []    # 线程队列
    Index = s["Index"][0]
    while threads or Index <= s["Index"][1]:
        for thread in threads:
            if not thread.is_alive():   # 线程不可用
                threads.remove(thread)  # 从线程队列中删掉
        while len(threads) < max_threads and Index <= s["Index"][1]:
            thread = threading.Thread(target=run, args=(Index, ))    # 创建线程
            thread.setDaemon(True)  # 设置守护线程
            thread.start()  # 启动线程
            print("thread start")
            time.sleep(1)
            threads.append(thread)  # 加入线程队列
            Index += 1


if __name__ == '__main__':
    crawl()
