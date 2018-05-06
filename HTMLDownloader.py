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
            'Connection': 'close',
        }
        try:
            r = requests.get(url, headers=headers, timeout=10)
            if r.status_code == 200:    # 访问正常
                return r.text
        except requests.exceptions.ConnectTimeout:      # 超时
            raise TimeoutError
        return None
