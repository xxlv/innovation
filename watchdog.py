#!/usr/bin/python
#-*- coding:utf-8 -*-

from btc import Btc


class WatchDog(object):

    def watching(self,coin,strategy):
        return strategy.run(Btc(coin))
