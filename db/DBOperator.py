#-*- coding: UTF-8 -*-
'''
Created on 2015-3-13
@author: Casey
'''
import MySQLdb
from db import LoggerFactory
import connectionpool
class DBOperator(object):

    def __init__(self):
        self.logger = LoggerFactory.getLogger('DBOperator')
        #self.conn = None

    def connDB(self):
        #单连接
        #self.conn=MySQLdb.connect(host="127.0.0.1",user="root",passwd="root",db="pystock",port=3307,charset="utf8")
        #连接池中获取连接
        self.conn=connectionpool.pool.connection()
        return self.conn
    def closeDB(self):
        if(self.conn != None):
            self.conn.close()


    def insertIntoDB(self, table, dict):
        try:
            if(self.conn != None):
                cursor = self.conn.cursor()
            else:
                raise MySQLdb.Error('No connection')

            sql = "insert into " + table + "("
            param = []
            for key in dict:
                sql += key + ','
                param.append(dict.get(key))
            param = tuple(param)
            sql = sql[:-1] + ") values("
            for i in range(len(dict)):
                sql += "%s,"
            sql = sql[:-1] + ")"

            self.logger.debug(sql % param)
            n = cursor.execute(sql, param)
            self.conn.commit()
            cursor.close()
        except MySQLdb.Error,e:
            self.logger.error("Mysql Error %d: %s" % (e.args[0], e.args[1]))
            self.conn.rollback()
    def execute(self, sql):
        try:
            if(self.conn != None):
                cursor = self.conn.cursor()
            else:
                raise MySQLdb.Error('No connection')

            n = cursor.execute(sql)
            return n
        except MySQLdb.Error,e:
            self.logger.error("Mysql Error %d: %s" % (e.args[0], e.args[1]))

    def findBySQL(self, sql):
        try:
            if(self.conn != None):
                cursor = self.conn.cursor()
            else:
                raise MySQLdb.Error('No connection')

            cursor.execute(sql)
            rows = cursor.fetchall()
            return rows
        except MySQLdb.Error,e:
            self.logger.error("Mysql Error %d: %s" % (e.args[0], e.args[1]))

    def findByCondition(self, table, fields, wheres):
        try:
            if(self.conn != None):
                cursor = self.conn.cursor()
            else:
                raise MySQLdb.Error('No connection')

            sql = "select "
            for field in fields:
                sql += field + ","
            sql = sql[:-1] + " from " + table + " where "

            param = []
            values = ''
            for where in wheres:
                sql += where.key + "='%s' and "
                param.append(where.value)
            param = tuple(param)
            self.logger.debug(sql)

            n = cursor.execute(sql[:-5] % param)
            self.conn.commit()
            cursor.close()
        except MySQLdb.Error,e:
            self.logger.error("Mysql Error %d: %s" % (e.args[0], e.args[1]))