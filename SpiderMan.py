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
s = Settings().setting
max_threads = 3
lock = threading.Lock()
base_url = "http://wenshu.court.gov.cn/CreateContentJS/CreateContentJS.aspx?DocID="


def crawl(Index):
    db.create_table()      # 创建表
    old_total = db.get_total()
    manager.add_docids(Index, db)

    def has_unvisited_id():
        return manager.get_docid(db)

    def go():
        docid = has_unvisited_id()
        lock.acquire()
        if docid:
            url = base_url + docid
            print(url)
            try:
                html = downloader.download(url)
                data = parser.parse(html)
                db.insert_into_db(data, docid)        # 插入数据库
            except TimeoutError:
                db.change_status(docid, -1)
            new_total = db.get_total()
            if (new_total - old_total) and (new_total - old_total) % 20 == 0:
                print("新增", new_total - old_total, "条")
        lock.release()

    threads = []    # 线程队列
    while threads or has_unvisited_id():
        for thread in threads:
            if not thread.is_alive():   # 线程不可用
                threads.remove(thread)  # 从线程队列中删掉
        while len(threads) < max_threads:
            thread = threading.Thread(target=go)    # 创建线程
            thread.setDaemon(True)  # 设置守护线程
            thread.start()  # 启动线程
            time.sleep(1)
            threads.append(thread)  # 加入线程队列
        time.sleep(1)


def process_crawler():
    process = []    # 进程队列
    cpu_nums = multiprocessing.cpu_count()
    print("将会启动进程数为：", cpu_nums)
    Index = s["Index"][0]
    while len(process) < cpu_nums and Index <= s["Index"][1]:
        p = multiprocessing.Process(target=crawl, args=(Index,))   # 创建进程
        p.start()   # 启动进程
        print("process starts")
        process.append(p)   # 加入进程队列
        Index += 1
    for p in process:
        p.join()    # 等待进程队列中进程结束
    db.close_cursor()  # 关闭数据库连接


if __name__ == '__main__':
    process_crawler()
