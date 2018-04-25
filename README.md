# wenshuSpider
  
![](https://img.shields.io/badge/requests-2.18.4-green.svg) ![](https://img.shields.io/badge/PyExecJS-1.5.1-green.svg) ![](https://img.shields.io/badge/beautifulsoup4-4.6.0-green.svg) ![](https://img.shields.io/badge/pymysql-0.7.9-green.svg)  
中国裁判文书网爬虫 —— http://wenshu.court.gov.cn

[GetAPI.py](https://github.com/ZTCooper/wenshuSpider/blob/master/GetAPI.py)		得到接口数据 <br>
[URLManager.py](https://github.com/ZTCooper/wenshuSpider/blob/master/URLManager.py)（URL管理器）		从接口数据提取DocID构造url <br>
[HTMLDownloader.py](https://github.com/ZTCooper/wenshuSpider/blob/master/HTMLDownloader.py)（HTML下载器） <br>
[HTMLParser.py](https://github.com/ZTCooper/wenshuSpider/blob/master/HTMLParser.py)（HTML解析器）		解析JSON数据和HTML <br>
[DataOutput.py](https://github.com/ZTCooper/wenshuSpider/blob/master/DataOutput.py)（数据存储器）存入MySQL <br>
[SpiderMan.py](https://github.com/ZTCooper/wenshuSpider/blob/master/SpiderMan.py)（爬虫调度器）		爬虫入口 <br><br>

```python SpiderMan.py``` 运行爬虫  
确保数据库中已有 *wenshu* 数据库（若没有：```CREATE DATABASE wenshu;```）   
DataOutput中设置数据库用户名，密码  
  

部分数据报错 *"Data too long for column 'title' at row 1"*
  
还没写完！！！
