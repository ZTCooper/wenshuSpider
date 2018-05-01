# encoding:utf-8
'''
author: ztcooper
contact: 1060214139@qq.com
LICENSE: MIT

下载页面
url = http://wenshu.court.gov.cn/CreateContentJS/CreateContentJS.aspx?DocID=" + id
'''
import requests
from random import choice
from settings import Settings


class HtmlDownloader(object):
    def __init__(self):
        self.u = Settings().user_agents

    def download(self, url):
        headers = {
            'User-Agent': choice(self.u),
        }
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            return r.text
        return None
