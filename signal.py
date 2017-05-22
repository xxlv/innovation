#!/usr/bin/python
#-*- coding:utf-8 -*-

class Signal(object):
    """
    信号
    """

    def __init__(self,price,nu,op,op_time):
        self.price=price
        self.nu=nu
        self.op=op
        self.op_time=op_time
        self.msg=[]
        self.money=0

    def setMoney(self,money):
        self.money=money

    def setMsg(self,msg):
        self.msg.append(msg)

    def getMsg(self):
        return self.msg

    def setPrice(self,price):
        self.price=price

    def setNu(self,nu):
        self.nu=nu

    def setOp(self,op):
        self.op=op

    def setOpTime(self,op_time):
        self.op_time=op_time

    def isBuy(self):
        return self.op > 0

    def isSell(self):
        return self.op < 0
