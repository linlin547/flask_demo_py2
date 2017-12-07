# -*- coding: utf-8 -*-
import MySQLdb,json
from DBUtils.PooledDB import PooledDB
from Mysql_operator import sql_manage as sm
pool = PooledDB(MySQLdb, mincached=15, maxcached=30, host='localhost', user='li', passwd='123456', db='Test',
                     port=3306, charset='utf8')
conn = pool.connection()
cur = conn.cursor()
post_params = {
        'name': u'中文',
        'url': 'http://127.0.0.1:2345/test/api/resultss',
        'expect_data': u"中文",
        'param': {"a":1,"b":2,"c":3,"test":u"中文"},
        'type':"post"
    }
param = json.dumps(post_params.get('param'))
expect_data = post_params.get('expect_data')
conf_sql = sm.insert_interface_conf % (post_params.get('name'), post_params.get('url'), str(param),expect_data,post_params.get('type'))
cur.execute(conf_sql)
conn.commit()
