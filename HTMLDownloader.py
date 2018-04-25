# encoding:utf-8
'''
下载页面
url = http://wenshu.court.gov.cn/CreateContentJS/CreateContentJS.aspx?DocID=" + id
'''
import requests


class HtmlDownloader(object):

    def download(self, url):
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299"}
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            return r.text
        return None
