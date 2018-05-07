# encoding:utf-8
'''
author: ztcooper(github)
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
import datetime
import threading
import multiprocessing


manager = UrlManager()
downloader = HtmlDownloader()
parser = HtmlParser()
s = Settings().setting
max_threads = 3
base_url = "http://wenshu.court.gov.cn/CreateContentJS/CreateContentJS.aspx?DocID="


# 逐条爬取
def crawl():
    db = DataOutput()   # 连接到数据库
    old_total = db.get_total()
    while db.has_unvisited():
        docid = manager.get_one_docid(db)
        url = base_url + docid
        for _ in range(3):
            try:
                html = downloader.download(url)
                data = parser.parse(html)
                db.insert_into_db(data, docid)        # 插入数据库
            except Exception as e:
                # print(e)
                error = e
                continue    # 若抛出异常，连续访问三次
            else:
                break       # 没有抛出异常，只访问一次
        else:       # forloop没有被break中断，即三次访问失败
            db.write_errors(docid, error)     # 写入错误日志
            db.delete_wrong_ids(docid)      # 从数据表中删除
        time.sleep(random())
    new_total = db.get_total()
    db.close_cursor()   # 关闭数据库
    print('新增', new_total - old_total, '条')


# 将需要爬取的docid存入数据库
def store_ids():
    db = DataOutput()   # 连接到数据库
    db.create_table()      # 创建表
    Page = s["Page"]    # 每页20条
    for region in s["regions"]:     # 每个地域
        for Order in s["Order"]:    # 排序标准
            for Direction in s["Direction"]:    # 升降序各深入100页
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
    db.close_cursor()   # 关闭数据库


# 获取今日新增
def today_new():
    db = DataOutput()       # 连接到数据库
    db.create_table()      # 创建表

    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    today = today.strftime('%Y-%m-%d')
    tomorrow = tomorrow.strftime('%Y-%m-%d')

    Page = s["Page"]
    Param = "上传日期:" + today + " TO " + tomorrow
    for Order in s["Order"]:    # 排序标准
        for Direction in s["Direction"]:    # 升降序各深入100页
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
    db.close_cursor()   # 关闭数据库


if __name__ == '__main__':
    print('获取url……')
    today_new()
    print('开始爬取……')
    crawl()
