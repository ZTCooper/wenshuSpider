# encoding:utf-8
'''
数据存储
'''
import pymysql


class DataOutput(object):
    # 实例化时连接到MySQL
    def __init__(self):
        self.datas = list()
        self.conn = pymysql.connect(host='127.0.0.1', port=3306,
                                    user='root', password='123456', db='wenshu', charset='gbk')
        self.cur = self.conn.cursor()

    def data_store(self, data):
        if not data:
            return
        self.datas.append(data)

    # 创建表
    def create_table(self):
        if not self.cur.execute("SHOW TABLES LIKE 'Info'"):     # 检查表是否已存在
            self.cur.execute(
                'CREATE TABLE Info (docid VARCHAR(50) NOT NULL PRIMARY KEY, title VARCHAR(255) NOT NULL, pubdate VARCHAR(20) NOT NULL, article TEXT NOT NULL);')

    # 查重
    def check_duplicates(self, id):
        self.cur.execute('SELECT COUNT(*) FROM info WHERE docid = "%s";' % id)
        return self.cur.fetchone()[0]

    # 插入数据
    def insert_into_db(self, data):
        errors = 0
        try:
            self.cur.execute('INSERT INTO Info(docid, title, pubdate, article) VALUES (%s, %s, %s, %s)',
                            (data['docid'], data['title'], data['pubdate'], data['article']))
        except Exception as e:
            errors += 1
        self.conn.commit()
        return errors

    # 关闭数据库连接
    def close_cursor(self):
        self.cur.close()
        self.conn.close()


'''
def test():
    s = DataOutput()
    item = {'title': '2', 'pubdate': '1', 'article': '0'}
    s.output_mysql(item)


if __name__ == '__main__':
    test()
'''
