# encoding:utf-8
'''
数据存储
'''
import pymysql


class DataOutput(object):
    def __init__(self):
        self.datas = list()

    def data_store(self, data):
        if not data:
            return
        self.datas.append(data)

    # 存入MySQL
    def output_mysql(self, item):
        conn = pymysql.connect(host='127.0.0.1', port=3306,
                               user='root', password='', db='wenshu')
        cur = conn.cursor()
        if not cur.execute("SHOW TABLES LIKE 'Info'"):
            cur.execute(
                'CREATE TABLE IF NOT EXISTS LIKE Info (title VARCHAR(50) NOT NULL, pubdate VARCHAR(20) NOT NULL, article TEXT NOT NULL);')
        for data in self.datas:
	        cur.execute('INSERT INTO Info(title, pubdate, article) VALUES (%s, %s, %s)',
	                    (data['title'], data['pubdate'], data['article']))
        conn.commit()
        cur.close()
        conn.close()


def test():
	s = DataOutput()
    item = {'title': '2', 'pubdate': '1', 'article': '0'}
    s.output_mysql(item)


if __name__ == '__main__':
    test()
