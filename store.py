#!/usr/bin/python
#-*- coding:utf-8 -*-

import pymysql
import os

CONN=pymysql.connect(
                host="127.0.0.1",
                user="root",
                passwd=os.environ['DB_PASS'],
                port=3306,
                db="innovation")

#  存储器
class Store(object):
    def __init__(self):
        self.store=CONN

    def execute(self,query,p=None):
        try:
            cursor=self.store.cursor()
            if p is not None:
                cursor.execute(query,p)
            else:
                cursor.execute(query)
            res=cursor.fetchall()
            cursor.close()
        except Exception as e:
            print(e)
            res=None

        self.store.commit()
        return res
