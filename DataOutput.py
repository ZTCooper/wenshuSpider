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

    # 获取docid以检查是否已访问过
    def get_old_docids(self):
        self.cur.execute('SELECT docid FROM info;')
        docids = self.cur.fetchall()
        return [docid[0] for docid in docids]

    # 插入数据
    def insert_into_db(self, data):
        erros = 0
        erros_messages = set()
        try:
            self.cur.execute('INSERT INTO Info(docid, title, pubdate, article) VALUES (%s, %s, %s, %s)',
                             (data['docid'], data['title'], data['pubdate'], data['article']))
        except Exception as e:
            erros += 1
            erros_messages.add(e)
        return erros, erros_messages
        '''
            print("Something goes wrong with database.")
            print(e)
        
        except pymysql.err.IntegrityError:
            print("已存在")
        '''
        self.conn.commit()

    # 关闭数据库连接
    def close_cursor(self):
        self.cur.close()
        self.conn.close()


def test():
    s = DataOutput()
    item = {'title': '2', 'pubdate': '1', 'article': '0'}
    s.output_mysql(item)


if __name__ == '__main__':
    test()
