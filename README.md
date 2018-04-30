# wenshuSpider
  
![](https://img.shields.io/badge/Python-3.6.3-blue.svg) ![](https://img.shields.io/badge/requests-2.18.4-green.svg) ![](https://img.shields.io/badge/PyExecJS-1.5.1-green.svg) ![](https://img.shields.io/badge/beautifulsoup4-4.6.0-green.svg) ![](https://img.shields.io/badge/pymysql-0.7.9-green.svg)    
  
中国裁判文书网爬虫 —— http://wenshu.court.gov.cn

[GetAPI.py](https://github.com/ZTCooper/wenshuSpider/blob/master/GetAPI.py)		获取接口数据（感谢[sixs](https://github.com/sixs/wenshu_spider)分享参数解密方法） <br>
[URLManager.py](https://github.com/ZTCooper/wenshuSpider/blob/master/URLManager.py)（URL管理器）		从接口数据提取DocID构造url <br>
[HTMLDownloader.py](https://github.com/ZTCooper/wenshuSpider/blob/master/HTMLDownloader.py)（网页下载器） <br>
[HTMLParser.py](https://github.com/ZTCooper/wenshuSpider/blob/master/HTMLParser.py)（HTML解析器）		解析JSON数据和HTML <br>
[DataOutput.py](https://github.com/ZTCooper/wenshuSpider/blob/master/DataOutput.py)（数据存储器）存入MySQL <br>
[SpiderMan.py](https://github.com/ZTCooper/wenshuSpider/blob/master/SpiderMan.py)（爬虫调度器）		爬虫入口 <br><br>

  
* 确保数据库中已有 *wenshu* 数据库（若没有：`CREATE DATABASE wenshu;`）   
* DataOutput中设置数据库用户名，密码  
* settings.py 中Index设置爬取页数及相关设置（Index = [m, n]表示爬取m到(n-1)页）  
  Page(每页条数) 只可设置为 5, 10, 15 或 20
* `python SpiderMan.py` 运行爬虫  <br><br>
<br>

##### 04/26/2018
* 修复部分数据报错 *"Data too long for column 'title' at row 1"*  （连接数据库时 `charset='gbk'`）
* 部分提取改用正则表达式，速度更快
* 增量式，利用数据库存储文书ID，构造url时去重  
  
##### 04/27/2018
* 修复查重时数据表不存在的错误
* 修改爬取页数的设置方式  
  
##### 04/28/2018
* 修改控制台输出为进度条（需安装第三方库PyPrind：`pip install pyprind`）
