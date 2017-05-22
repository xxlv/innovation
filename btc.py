#!/usr/bin/python
#-*- coding:utf-8 -*-

import requests
import json
import time
import pymysql
import os

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
