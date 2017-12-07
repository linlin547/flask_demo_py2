# -*- coding: utf-8 -*-
import MySQLdb
import _mysql_exceptions
from DBUtils.PooledDB import PooledDB
from Mysql_operator import *
class Mysql_Manage:
    def __init__(self):
        # 连接池里的最少15连接,最大30个连接
        self.pool = PooledDB(MySQLdb, mincached=minthread, maxcached=maxthread, host='localhost', user=my_user, passwd=my_pwd, db=my_DB, port=my_port, charset='utf8')
        self.conn = self.pool.connection()  # 以后每次需要数据库连接就是用connection（）函数获取连接就好了
        self.cur = self.conn.cursor()
    def query_data(self, sql):
        self.cur.execute(sql)
        return self.cur.fetchall()
    def insert_data(self, sql):
        try:
            self.cur.execute(sql)
            self.conn.commit()
        except _mysql_exceptions.IntegrityError:
            # name重复
            return 0
        except Exception,e:
            return 1

    def delete_data(self, sql):
        self.cur.execute(sql)
        self.conn.commit()

    # def close_sql(self):
    #     self.cur.close()
    #     self.conn.close()