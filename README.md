# wenshuSpider
中国裁判文书网爬虫 —— http://wenshu.court.gov.cn

[GetAPI.py](https://github.com/ZTCooper/wenshuSpider/blob/master/GetAPI.py)		得到接口数据
[URLManager.py](https://github.com/ZTCooper/wenshuSpider/blob/master/URLManager.py)（URL管理器）		从接口数据提取DocID构造url
[HTMLDownloader.py](https://github.com/ZTCooper/wenshuSpider/blob/master/HTMLDownloader.py)（HTML下载器）
[HTMLParser.py](https://github.com/ZTCooper/wenshuSpider/blob/master/HTMLParser.py)（HTML解析器）		解析JSON数据和HTML
[DataOutput.py](https://github.com/ZTCooper/wenshuSpider/blob/master/DataOutput.py)（数据存储器）
[SpiderMan.py](https://github.com/ZTCooper/wenshuSpider/blob/master/SpiderMan.py)（爬虫调度器）		爬虫入口
