#-*- coding: UTF-8 -*-
'''
create a connection pool
'''
from DBUtils import PooledDB
import MySQLdb
import string
maxconn = 30            #最大连接数
mincached = 10           #最小空闲连接
maxcached = 20          #最大空闲连接
maxshared = 30          #最大共享连接
connstring="johnson#plokij#127.0.0.1#3306#Quant#utf8" #数据库地址
dbtype = "mysql"                   #选择mysql作为存储数据库
def createConnectionPool(connstring, dbtype):
    db_conn = connstring.split("#");
    if dbtype=='mysql':
        try:
            pool = PooledDB.PooledDB(MySQLdb, user=db_conn[0],passwd=db_conn[1],host=db_conn[2],port=string.atoi(db_conn[3]),db=db_conn[4],charset=db_conn[5], mincached=mincached,maxcached=maxcached,maxshared=maxshared,maxconnections=maxconn)
            return pool
        except Exception, e:
            raise Exception,'conn datasource Excepts,%s!!!(%s).'%(db_conn[2],str(e))
            return None
pool = createConnectionPool(connstring, dbtype)