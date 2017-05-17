#!/usr/bin/python

import requests
import json
import time

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

class WatchDog(object):
    def watching(self,coin,task):
        task.run(Btc(coin))
# 策略组合
class Task(object):
    def run(self,o):
        return self.reportCurrentStats(o)

    def reportCurrentStats(self,o):
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

(WatchDog()).watching("btc",Task())
