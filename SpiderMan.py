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


class SpiderMan(object):
    def __init__(self):
        self.manager = UrlManager()
        self.downloader = HtmlDownloader()
        self.parser = HtmlParser()
        self.output = DataOutput()  # 实例化时连接到数据库
        self.s = Settings().setting

    def crawl(self):
        self.output.create_table()      # 创建表
        total_page = self.s["Index"][1] - self.s["Index"][0]
        total_data = total_page * self.s["Page"]
        total_errors = 0
        total_duplicates = 0
        old_total = self.output.get_total()

        for Index in range(self.s["Index"][0], self.s["Index"][1]):
            duplicates = self.manager.add_urls(Index, self.output)
            urls = self.manager.get_urls()
            bar = pyprind.ProgBar(
                self.s["Page"] - duplicates, title="Crawling " + "Page " + str(Index) + " ......")   # 进度条
            for url in urls:
                try:
                    bar.update()
                    html = self.downloader.download(url)
                    data = self.parser.parse(html)
                    self.output.insert_into_db(data)        # 插入数据库
                except Exception:
                    continue
        new_total = self.output.get_total()
        self.output.close_cursor()  # 关闭数据库连接

        print("本次爬取", new_total - old_total, "条")


if __name__ == '__main__':
    spider_man = SpiderMan()
    spider_man.crawl()
