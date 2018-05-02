中国裁判文书网爬虫
==============================
  
![](https://img.shields.io/badge/Python-3.6.3-blue.svg) ![](https://img.shields.io/badge/requests-2.18.4-green.svg) ![](https://img.shields.io/badge/PyExecJS-1.5.1-green.svg) ![](https://img.shields.io/badge/beautifulsoup4-4.6.0-green.svg) ![](https://img.shields.io/badge/pymysql-0.7.9-green.svg) ![](https://img.shields.io/badge/PyPrind-2.11.2-green.svg)    
  
中国裁判文书网——http://wenshu.court.gov.cn  
  
  
使用说明
-------------------------
* DataOutput中设置数据库用户名，密码 
* 确保数据库中已有 *wenshu* 数据库（若没有：`CREATE DATABASE wenshu;`）   
* settings.py 中及相关设置  
* `python SpiderMan.py` 运行爬虫  <br>

特别说明
-------------------
关于**settings.py**的设置：
* Param: 搜索关键字。默认为"全文检索:\*"，可设置为"案件类型:\*"， "文书类型:\*"等等，星号可替换为具体关键字，具体参考文书网首页 高级检索 栏。
* Index：爬取页数。Index = [m, n]表示爬取m到n页。
* Page：每页条数。只可设置为 5, 10, 15 或 20。
* Order：排序标准。可设置为"法院层级"，"裁判日期" 或 "审判程序"。
* Direction: 升序降序。"asc"正序，"desc"倒序。**如设置"Order": "裁判日期"， "Direction": "desc"可爬取最新文书**。
<br>

代码简单说明
-------------
[GetAPI.py](https://github.com/ZTCooper/wenshuSpider/blob/master/GetAPI.py)		获取接口数据（感谢[sixs](https://github.com/sixs/wenshu_spider)分享参数解密方法） <br>
[URLManager.py](https://github.com/ZTCooper/wenshuSpider/blob/master/URLManager.py)（URL管理器）		从接口数据提取DocID构造url（构造过程略慢……QAQ） <br>
[HTMLDownloader.py](https://github.com/ZTCooper/wenshuSpider/blob/master/HTMLDownloader.py)（网页下载器） <br>
[HTMLParser.py](https://github.com/ZTCooper/wenshuSpider/blob/master/HTMLParser.py)（HTML解析器）		解析JSON数据和HTML <br>
[DataOutput.py](https://github.com/ZTCooper/wenshuSpider/blob/master/DataOutput.py)（数据存储器）存入MySQL <br>
[SpiderMan.py](https://github.com/ZTCooper/wenshuSpider/blob/master/SpiderMan.py)（爬虫调度器）		爬虫入口 <br><br>

To do
-----------
* 每个搜索条件下只能爬取到100页，100以后访问接口返回数据为空。浏览器手动翻到26页提示“返回结果过多，推荐精准检索后查询”。

Let me know
-------------------------
在运行中出现问题或有好的提议请通过 *Issues* 告诉我，或通过 qq(1060214139)， email 联系我。 XD<br>
创建本项目主要为学习交流，技术不成熟，希望在学习的过程中完善，请多多指教。  <br><br>

Update Log
--------------------------
##### 04/26/2018
* 修复部分数据报错 *"Data too long for column 'title' at row 1"*  （连接数据库时 `charset='gbk'`）
* 部分提取改用正则表达式，速度更快
* 增量式，利用数据库存储文书ID，构造url时去重  
  
##### 04/27/2018
* 修复查重时数据表不存在的错误
* 修改爬取页数的设置方式  
  
##### 04/28/2018
* 修改控制台输出为进度条（需安装第三方库PyPrind：`pip install pyprind`） 
  
##### 05/01/2018
* 增加 User-Agent pool  
