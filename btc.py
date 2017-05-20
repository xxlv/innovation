#!/usr/bin/python
#-*- coding:utf-8 -*-

import requests
import json
import time
import pymysql


CONN=pymysql.connect(
                host="127.0.0.1",
                user="root",
                passwd="",
                port=3306,
                db="innovation")


# BTC core
class Btc(object):
    def __init__(self,coin):
        self.coin=coin
        self.api="http://api.btctrade.com/api/{}"

    def getCurrentDepth(self):
        url=self.api.format("depth?coin={}".format(self.coin))
        data=self.__doGet(url)
        return data

    # Return current states
    def getStates(self):
        url=self.api.format("ticker?coin={}".format(self.coin))
        data=self.__doGet(url)
        return data

    def __doGet(self,url):
        return json.loads(requests.get(url).content.decode())

# 监视器
class WatchDog(object):
    def watching(self,coin,task):
        return task.run(Btc(coin))

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



class Master(object):
    def buy(self):
        pass

    def sell(self):
        pass


# 策略组合
class Task(object):
    def __init__(self):
        self.store=Store()

    def run(self,o):
        recorded=self.record(o)
        signal=self.s1(o)
        avg=self.getAverage(o)

        if int(time.time())-self.getCurrentNotificationTime() <= 5*60:
            # 5分钟通知一次
            return None

        if(signal==1):
            self.markAsNotification()
            return "#{}[s1]# 发现一波短线机会，平均高为{} \n\n {}".format(o.coin,avg[0],self.reportCurrentStates(o))

        if(signal==-1):
            self.markAsNotification()
            return "#{}[s1]# 糟糕，情况不对，平均低位{}, 请尽快平仓\n\n {}".format(o.coin,avg[1],self.reportCurrentStates(o))
        return None


    def markAsNotification(self):
        # clean
        self.store.execute("DELETE FROM notification where 1=1")

        sql="""
        INSERT INTO notification (`current_time_cursor`) values(%s)
        """
        return self.store.execute(sql,(int(time.time())))




    def getCurrentNotificationTime(self):

        sql="""
        SELECT current_time_cursor FROM notification LIMIT 1
        """
        curr=self.store.execute(sql)
        if curr is not None:
            currTime=curr[0][0]
        else:
            currTime=0

        return currTime

    def record(self,o):
        # 记录当前时间价格
         record=o.getStates()
         record['type']=o.coin


         data=[str(x) for x in record.values()]
         sql="""
           INSERT INTO `b` (`high`,`low`,`buy`,`sell`,`last`,`vol`,`time`,`type`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
         """

         return self.store.execute(sql,tuple(data))

    def getAverage(self,o,day=5):
        # current time
        target=int(time.time())-day*24*60*60

        sql="""
        SELECT AVG(high),AVG(low) FROM b WHERE `time` > {} AND `type`= '{}'
        """.format(target,o.coin)
        avgPrice=self.store.execute(sql)
        return avgPrice[0]


    # 短线交易策略 s1
    # v1.0
    # 检测当前的买入点是否在平均五日线上方，则释放买入信号
    # 检测当前的卖出掉是否在平均五日线的下方，则释放卖出信号
    # TODO 增加浮动策略
    def s1(self,o):
        signal=0
        states=o.getStates()
        avgPrice=self.getAverage(o,5)
        if (avgPrice[0]!=None and states['high']>=avgPrice[0]):
            signal=1
        if(avgPrice[1]!=None and states['low']<=avgPrice[1]):
            signal=-1
        return signal



    def reportCurrentStates(self,o):
        states=o.getStates()
        msg=" 最高价: {}\n 最低价：{} \n 买一价：{}\n 卖一价：{}\n 最新成交价:{} \n 成交量：{}\n 时间：{}".format(
        states['high'],
        states['low'],
        states['buy'],
        states['sell'] ,
        states['last'],
        states['vol'],
        time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(states['time']))
        )

        return msg



(WatchDog()).watching("ltc",Task())
