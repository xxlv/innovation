#!/usr/bin/python
#-*- coding:utf-8 -*-

import random
import hashlib
import requests
import hmac
import time
import os
import json

from util import http_post

# 操盘手
class Trander(object):

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
        return json.loads(data)



    # 挂单买入
    def buy(self,signal):

        param=dict()
        param['amount']=signal.nu
        param['price']=signal.price

        data=self._post(self.api.format('buy/'),self._package(param))
        return json.loads(data)


    # 挂单卖出
    def sell(self,signal):

        param=dict()
        param['amount']=signal.nu
        param['price']=signal.price
        data=self._post(self.api.format('sell/'),self._package(param))

        return json.loads(data)

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
        return http_post(url,params)
