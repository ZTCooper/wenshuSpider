中国裁判文书网爬虫
==============================
  
![](https://img.shields.io/badge/Python-3.6.3-blue.svg) ![](https://img.shields.io/badge/requests-2.18.4-green.svg) ![](https://img.shields.io/badge/PyExecJS-1.5.1-green.svg) ![](https://img.shields.io/badge/beautifulsoup4-4.6.0-green.svg) ![](https://img.shields.io/badge/pymysql-0.7.9-green.svg)    
  
中国裁判文书网——http://wenshu.court.gov.cn  
  
  
使用说明
-------------------------
* DataOutput中设置数据库用户名，密码 
* 确保数据库中已有 *wenshu* 数据库（若没有：`CREATE DATABASE wenshu;`），不需要创建数据表，首次运行会创建数据表info：  
（**05/06/2018 修改数据表结构：**  
新增status字段（2:正在访问；1:访问成功且插入正常；0:未访问；-1:访问超时或插入异常；)  
和region（地域）字段）:  

	| Field   | Type         | Null | Key | Default | Extra |
	| -       | :-:          | :-:  | :-: | :-:     | -:    |
	| docid   | varchar(50)  | NO   | PRI | NULL    |       |
	| status  | int(11)      | NO   |     | 0       |       |
	| region  | varchar(50)  | NO   |     | NULL    |       |
	| title   | varchar(255) | YES  |     | NULL    |       |
	| pubdate | varchar(20)  | YES  |     | NULL    |       |
	| article | text         | YES  |     | NULL    |       |   

* ~~settings.py 中进行相关设置~~  
* `python SpiderMan.py` 运行爬虫  <br>

特别说明
-------------------
关于**settings.py**的设置：
* Param: 搜索关键字。默认为"法院地域:"~~，可设置为"案件类型:\*"， "文书类型:\*"等等，星号可替换为具体关键字，具体参考文书网首页 高级检索 栏。~~
* Index：爬取页数。Index = [m, n]表示爬取m到n页（默认1~100页，目前仅能爬到100页）。
* Page：每页条数。只可设置为 5, 10, 15 或 20（建议20）。
* Order：排序标准。~~可设置为"法院层级"，"裁判日期" 或 "审判程序"。~~
* Direction: 升序降序。"asc"正序，"desc"倒序。~~**如设置"Order": "裁判日期"， "Direction": "desc"可爬取最新文书**。~~
<br>

代码简单说明
-------------
* [GetAPI.py](https://github.com/ZTCooper/wenshuSpider/blob/master/GetAPI.py)：访问列表页接口获得数据，每次访问一页默认可获得20条DocID（感谢[sixs](https://github.com/sixs/wenshu_spider)分享参数解密方法） <br>
* [URLManager.py](https://github.com/ZTCooper/wenshuSpider/blob/master/URLManager.py)（URL管理器）：  		将上一步获取的数据中提取的DocID和地域存入数据库，status默认为0（未爬取） <br>  
* [HTMLDownloader.py](https://github.com/ZTCooper/wenshuSpider/blob/master/HTMLDownloader.py)（网页下载器） <br>
* [HTMLParser.py](https://github.com/ZTCooper/wenshuSpider/blob/master/HTMLParser.py)（HTML解析器）：  		解析JSON数据和HTML，提取需要字段（标题，日期，正文） <br>
* [DataOutput.py](https://github.com/ZTCooper/wenshuSpider/blob/master/DataOutput.py)（数据存储器）：存入MySQL <br>
* [SpiderMan.py](https://github.com/ZTCooper/wenshuSpider/blob/master/SpiderMan.py)（爬虫调度器）：	爬虫入口，首先执行**store_id()**将需要爬取的文书id存入（**若爬取今日新增则执行today_new()**），然后执行**crawl()**，从数据库中取出未访问或访问异常的docid构造url（正文页采用了Ajax） <br><br>
由于目前每个搜索条件下仅能深入到100页，所以循环遍历搜索条件可得到尽量多的数据，这样每个地域可得到不超过12000篇文书，共32个地域
```python
Page = s["Page"]	# 每页20条
    for region in s["regions"]:		# 每个地域
        for Order in s["Order"]:	# 排序标准
            for Direction in s["Direction"]:	# 升降序各深入100页
                Param = s["Param"] + region
```


To do
-----------
* 运行过程由于频繁访问会中断，后续会增加代理IP池，有需要可参考我之前使用scrapy框架写的[西刺免费代理IP爬虫](https://github.com/ZTCooper/crawler-scrapy/tree/master/proxy)
* 每个搜索条件下只能爬取到100页，100以后访问接口返回数据为空。浏览器手动翻到26页提示“返回结果过多，推荐精准检索后查询”。

Contact me
-------------------------
在运行中出现问题或有好的提议请通过 [Issues](https://github.com/ZTCooper/wenshuSpider/issues/new) 告诉我，或通过 qq(1060214139)， email 联系我。<br>
创建本项目主要为学习交流，技术不成熟，希望在学习的过程中完善，请多多指教。  <br><br>

Update Log
--------------------------
##### 05/06/2018
* 列表页接口访问改用多线程
* 数据表新增status（存储访问状态）和region字段，改为从数据库中提取未访问或异常状态的docid构造url
* 可按地域遍历爬取
* 新增爬取“今日新增”文书  

##### 05/01/2018
* 增加 User-Agent pool  

##### 04/28/2018
* ~~修改控制台输出为进度条（需安装第三方库PyPrind：`pip install pyprind`）~~  

##### 04/27/2018
* 修复查重时数据表不存在的错误
* 修改爬取页数的设置方式 

##### 04/26/2018
* 修复部分数据报错 *"Data too long for column 'title' at row 1"*  （连接数据库时 `charset='gbk'`）
* 部分提取改用正则表达式，速度更快
* 增量式，利用数据库存储文书ID，构造url时去重  
  
 
  
 
  
  
