# encoding:utf-8
'''
爬虫调度器（入口）
'''
from URLManager import UrlManager
from HTMLDownloader import HtmlDownloader
from HTMLParser import HtmlParser
from DataOutput import DataOutput
import pyprind


class SpiderMan(object):
    def __init__(self):
        self.manager = UrlManager()
        self.downloader = HtmlDownloader()
        self.parser = HtmlParser()
        self.output = DataOutput()  # 实例化时连接到数据库

    def crawl(self):
        self.output.create_table()      # 创建表
        self.manager.add_new_urls()     # 创建url
        total = self.manager.new_urls_size()
        bar = pyprind.ProgBar(30, title="Crawling......")   # 进度条
        while (self.manager.new_urls_size()):
            url = self.manager.get_new_url()
            html = self.downloader.download(url)
            data = self.parser.parse(html)
            errors, errors_messages = self.output.insert_into_db(
                data)        # 插入数据库
            bar.update()
            '''
            sys.stdout.write(
                str(self.manager.old_urls_size() / total * 100) + "%")
            sys.stdout.flush()
            # print('爬取', self.manager.old_urls_size(), '条。')
            '''
        self.output.close_cursor()  # 关闭数据库连接
        print("本次共爬取", total, "条")
        if errors:
            print("其中", errors, "条数据出错")
            print("错误：" + str(errors_messages))


if __name__ == '__main__':
    spider_man = SpiderMan()
    spider_man.crawl()
