#!/usr/bin/python
#-*- coding:utf-8 -*-

import random
import hashlib
import requests
import hmac
import time
import os


# 操盘手
class Trandder(object):

    # 初始化配置
    def __init__(self,coin='doge'):

        self.pub_key=str(os.environ['COIN_PUB_KEY'])
        self.pri_key=str(os.environ['COIN_PRI_KEY'])
        self.coin=coin
        self.version=2
        self.api="http://api.btctrade.com/api/{}"

    # 设置币种
    def setCoin(self,coin):

        self.coin=coin

    # 参数打包
    def _package(self,p=dict()):

        p['coin']=self.coin
        p['key']=self.pub_key
        p['version']=self.version
        p['nonce']=time.time()

        params=""
        _index=0
        for k,v in p.items():
            _index=_index+1
            if _index>=len(p):
                params+="{}={}".format(k,v)
            else:
                params+="{}={}&".format(k,v)

        k=hashlib.md5(self.pri_key.encode('utf-8')).hexdigest().encode("utf-8")
        signature = hmac.new(bytes(k), params.encode('utf-8'), digestmod=hashlib.sha256).hexdigest()
        p['signature']=signature
        return p

    # 获取账户信息
    def balance(self):

        param=dict()
        api=self.api.format('balance/')
        package=self._package(param)
        data=self._post(api,package)
        return data.content.decode('utf-8')



    # 挂单买入
    def buy(self,amount,price):

        param=dict()
        param['amount']=amount
        param['price']=price
        api=self.api.format('buy/')
        package=self._package(param)
        data=self._post(api,package)
        return data

    # 挂单卖出
    def sell(self):

        param=dict()
        param['amount']=amount
        param['price']=price
        api=self.api.format('sell/')
        package=self._package(param)
        data=self._post(api,package)
        return data

    # 取消挂单
    def cancel_order(self,order_id):
        param=dict()
        param['id']=order_id
        api=self.api.format('cancel_order/')
        package=self._package(param)
        data=self._post(api,package)
        return data

    # POST
    def _post(self,url,params):
        return requests.post(url,params)


t=Trandder()
info=t.balance()
print(info)
