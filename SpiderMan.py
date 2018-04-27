# encoding:utf-8
'''
爬虫调度器（入口）
'''
from URLManager import UrlManager
from HTMLDownloader import HtmlDownloader
from HTMLParser import HtmlParser
from DataOutput import DataOutput


class SpiderMan(object):
    def __init__(self):
        self.manager = UrlManager()
        self.downloader = HtmlDownloader()
        self.parser = HtmlParser()
        self.output = DataOutput()  # 实例化时连接到数据库

    def crawl(self):
        self.output.create_table()      # 创建表
        self.manager.add_new_urls()		# 创建url
        while (self.manager.new_urls_size()):
            url = self.manager.get_new_url()
            html = self.downloader.download(url)
            data = self.parser.parse(html)
            self.output.insert_into_db(data)		# 插入数据库
            print('爬取', self.manager.old_urls_size(), '条。')
        self.output.close_cursor()	# 关闭数据库连接


if __name__ == '__main__':
    spider_man = SpiderMan()
    spider_man.crawl()
