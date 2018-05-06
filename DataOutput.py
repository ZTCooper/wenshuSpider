# encoding:utf-8
'''
author: ztcooper
contact: 1060214139@qq.com
LICENSE: MIT

数据存储

数据表info
+---------+--------------+------+-----+---------+-------+
| Field   | Type         | Null | Key | Default | Extra |
+---------+--------------+------+-----+---------+-------+
| docid   | varchar(50)  | NO   | PRI | NULL    |       |
| status  | int(11)      | NO   |     | 0       |       |
| region  | varchar(50)  | NO   |     | NULL    |       |
| title   | varchar(255) | YES  |     | NULL    |       |
| pubdate | varchar(20)  | YES  |     | NULL    |       |
| article | text         | YES  |     | NULL    |       |
+---------+--------------+------+-----+---------+-------+
status ---> 2:正在访问；1:访问成功且插入正常；0:未访问；-1:访问超时或插入异常；
'''

import pymysql


class DataOutput(object):
    # 实例化时连接到MySQL
    def __init__(self):
        self.datas = list()
        self.conn = pymysql.connect(host='127.0.0.1', port=3306,
                                    user='root', password='123456', db='wenshu', charset='gbk')
        self.cur = self.conn.cursor()

    # 存入docid
    def insert_docid(self, docid, region):
        try:
            self.cur.execute(
                'INSERT INTO info (docid, region) VALUES (%s, %s)', (docid, region))
        except Exception as e:
            pass
        self.conn.commit()

    # 创建表
    def create_table(self):
        if not self.cur.execute("SHOW TABLES LIKE 'Info'"):     # 检查表是否已存在
            self.cur.execute(
                'CREATE TABLE Info (docid VARCHAR(50) NOT NULL PRIMARY KEY, status INT NOT NULL DEFAULT 0, region VARCHAR(50) NOT NULL, title VARCHAR(255), pubdate VARCHAR(20), article TEXT);')

    # 获得数据量
    def get_total(self):
        self.cur.execute('SELECT COUNT(*) FROM info WHERE status = 1')
        return self.cur.fetchone()[0]

    # 还有未访问成功的链接
    def has_unvisited(self):
        self.cur.execute('SELECT COUNT(*) FROM info WHERE status != 1')
        return self.cur.fetchone()[0]

    # 修改状态（2:正在访问；1:访问成功且插入正常；0:未访问；-1:访问超时或插入异常；）
    def change_status(self, docid, status):
        self.cur.execute(
            'UPDATE info SET status = %d WHERE docid = "%s";' % (status, docid))

    # 插入数据
    def insert_into_db(self, data, docid):
        self.cur.execute('UPDATE info SET status = 1, region = "%s", title = "%s", pubdate = "%s", article = "%s" WHERE docid = "%s";' % (
            data['region'], data['title'][0], data['pubdate'][0], data['article'], docid))
        self.conn.commit()

    # 删除异常数据
    def delete_wrong_ids(self, docid):
        self.cur.execute('DELETE FROM info WHERE docid = "%s";' % docid)

    # 关闭数据库连接
    def close_cursor(self):
        self.cur.close()
        self.conn.close()
