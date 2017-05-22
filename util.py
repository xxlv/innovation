#!/usr/bin/python
#-*- coding:utf-8 -*-

import requests

PROXY_POOL={
}

PROXY_POOL=None


def http_get(url):
    return requests.get(url,proxies=PROXY_POOL).content.decode()

def http_post(url,params):
    return requests.post(url,params,proxies=PROXY_POOL).content.decode('utf-8')
