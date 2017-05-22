#!/usr/bin/python
#-*- coding:utf-8 -*-

import time
from store import Store
from signal import Signal
from trander import Trander

class DogStrategy(object):

    def __init__(self):
        self.buyPoint=0.0194
        self.p_of_keep=0.001
        self.store=Store()



    def run(self,o):
        return self.s2_of_dog(o)


    def set_curr_keep_price_empty(self):

        sql="""
        DELETE FROM keep WHERE 1=1
        """
        return self.store.execute(sql)


    def get_curr_keep(self):
        sql="""
        SELECT price,nu FROM keep WHERE coin='doge' ORDER BY id DESC
        """
        r= self.store.execute(sql)

        if r and r is not None:
            price= r[0][0]
            nu=r[0][1]
        else:
            price= 0
            nu=0

        return {"price":price,"nu":nu}

    def set_curr_keep_price(self,data):
        sql="""
        INSERT INTO keep(coin,nu,price,created_at) values(%s,%s,%s,%s);
        """
        return self.store.execute(sql,data)

    def get_how_much_money_i_make(self,o):
        curr=o.getStates()

        price=curr['sell']
        curr_keep=self.get_curr_keep()
        curr_keep_nu=int(curr_keep['nu'])
        curr_keep_price=float(curr_keep['price'])
        money=int(price*curr_keep_nu-curr_keep_price*curr_keep_nu)-int(price*curr_keep_nu-curr_keep_price*curr_keep_nu)*self.p_of_keep
        return money


    # 狗狗币策略
    # 损失接近止损点 则警告卖出
    # 收益超过止盈点 则提示
    def s2_of_dog(self,o):

        # 止损点
        miss_point=-50
        # 止盈点
        warm_point=200
        msg=[]
        o.coin='doge'
        curr=o.getStates()
        sell=curr['buy']

        # 持仓价格
        current_keep_price=1.0
        # 手续费率
        p_of_keep=self.p_of_keep
        # 持仓数
        nu_of_keep=1
        # 持仓成本
        nu_of_keep_price=nu_of_keep*current_keep_price
        # 手续费
        nu_of_keep_miss_price=nu_of_keep_price*p_of_keep
        # 当前盈利
        curr_draw=(nu_of_keep*sell)-(nu_of_keep_price+nu_of_keep_miss_price)
        # 实时收益率
        rate_of_return=(curr_draw/nu_of_keep_price)*100
        # 默认操作信号 0 不处理
        op=0
        nu=nu_of_keep
        price=curr['high']

        # if(curr_draw > warm_point or rate_of_return > 5):
        #     # 卖出信号
        #     op=-1
        #     msg.append("恭喜，当前收益为{} ,收益率为{}".format(curr_draw,rate_of_return))
        #
        # if(curr_draw < miss_point):
        #     # 卖出信号
        #     op=-1
        #     msg.append("不好，损失({}) 已抵达止损点{},请尽快处理。收益率为{}".format(curr_draw,miss_point,rate_of_return))
        money=0
        # 检查当前的价格处于可接受范围内
        # print(curr)
        t=Trander()


        if(curr['buy']<=self.buyPoint):
            price=curr['buy']
            t=Trander()
            my=t.balance()
            my_money=float(my['cny_balance'])
            can_buy_nu=int(my_money/price)-int(my_money/price)*self.p_of_keep
            # TODO
            nu=can_buy_nu

            if(self.get_curr_keep()['price'] != '0' and self.get_curr_keep()['price'] != 0):
                op=0
            else:
                # self.set_curr_keep_price(['doge',can_buy_nu,price,int(time.time())])
                op=1

        money=self.get_how_much_money_i_make(o)
        # print(curr_keep_price- curr['sell'])
        # print(curr_keep_price)
        # print(curr['sell'])
        if(money > 10):
            # 计算收益
            price=curr['sell']
            curr_keep=self.get_curr_keep()
            curr_keep_nu=int(curr_keep['nu'])
            curr_keep_price=float(curr_keep['price'])
            money=int(price*curr_keep_nu-curr_keep_price*curr_keep_nu)
            nu=curr_keep_nu
            # self.set_curr_keep_price_empty()
            op=-1

        s=Signal(price,nu,op,time.time())
        s.setMsg(msg)
        s.setMoney(money)

        return s


#
# # 策略组合
# class Strategy(object):
#
#     #
#     def __init__(self):
#         self.store=Store()
#
#     # 信息
#     def run(self,o):
#         msg=[]
#         # record
#         recorded=self.record(o)
#         s1_msg=self.s1(o)
#         s2_dog_msg=self.s2_of_dog(o)
#
#         if s1_msg:
#             msg.append(s1_msg)
#         if s2_dog_msg:
#             msg.append(s2_dog_msg)
#
#         return "".join(msg)
#
#
#     def markAsNotification(self):
#         # clean
#         self.store.execute("DELETE FROM notification where 1=1")
#
#         sql="""
#         INSERT INTO notification (`current_time_cursor`) values(%s)
#         """
#         return self.store.execute(sql,(int(time.time())))
#
#     def getCurrentNotificationTime(self):
#         sql="""
#         SELECT current_time_cursor FROM notification LIMIT 1
#         """
#         curr=self.store.execute(sql)
#         if curr is not None:
#             currTime=curr[0][0]
#         else:
#             currTime=0
#
#         return currTime
#
#     def record(self,o):
#         # 记录当前时间价格
#          record=o.getStates()
#          record['type']=o.coin
#          data=[str(x) for x in record.values()]
#          sql="""
#            INSERT INTO `b` (`high`,`low`,`buy`,`sell`,`last`,`vol`,`time`,`type`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
#          """
#
#          return self.store.execute(sql,tuple(data))
#
#     def getAverage(self,o,day=5):
#         # current time
#         target=int(time.time())-day*24*60*60
#
#         sql="""
#         SELECT AVG(high),AVG(low) FROM b WHERE `time` > {} AND `type`= '{}'
#         """.format(target,o.coin)
#         avgPrice=self.store.execute(sql)
#         return avgPrice[0]
#
#
#     # 短线交易策略 s1
#     # v1.0
#     # 检测当前的买入点是否在平均五日线上方，则释放买入信号
#     # 检测当前的卖出掉是否在平均五日线的下方，则释放卖出信号
#     # TODO 增加浮动策略
#     def s1(self,o):
#         signal=0
#         states=o.getStates()
#         avgPrice=self.getAverage(o,5)
#         if (avgPrice[0]!=None and states['high']>=avgPrice[0]):
#             signal=1
#         if(avgPrice[1]!=None and states['low']<=avgPrice[1]):
#             signal=-1
#
#         if int(time.time())-self.getCurrentNotificationTime() <= 5*60:
#             # 5分钟通知一次
#             return ""
#
#         if(signal==1):
#             self.markAsNotification()
#             return "#{}[s1]# 发现一波短线机会，平均高为{} \n\n {}".format(o.coin,avgPrice[0],self.reportCurrentStates(o))
#
#         if(signal==-1):
#             self.markAsNotification()
#             return "#{}[s1]# 糟糕，情况不对，平均低位{}, 请尽快平仓\n\n {}".format(o.coin,avgPrice[1],self.reportCurrentStates(o))
#
#         return ""
#
#
#     # 狗狗币策略
#     # 损失接近止损点 则警告卖出
#     # 收益超过止盈点 则提示
#     def s2_of_dog(self,o):
#
#         # 止损点
#         miss_point=-50
#         # 止盈点
#         warm_point=200
#         msg=[]
#         o.coin='doge'
#         curr=o.getStates()
#         sell=curr['buy']
#
#         # 持仓价格
#         current_keep_price=0.0126
#         # 手续费率
#         p_of_keep=0.001
#         # 持仓数
#         nu_of_keep=39650.554
#         # 持仓成本
#         nu_of_keep_price=nu_of_keep*current_keep_price
#         # 手续费
#         nu_of_keep_miss_price=nu_of_keep_price*p_of_keep
#         # 当前盈利
#         curr_draw=(nu_of_keep*sell)-(nu_of_keep_price+nu_of_keep_miss_price)
#         # 实时收益率
#         rate_of_return=(curr_draw/nu_of_keep_price)*100
#
#         print(curr_draw)
#
#         if int(time.time())-self.getCurrentNotificationTime() <= 5*60:
#             # 5分钟通知一次
#             return ""
#
#         if(curr_draw > warm_point or rate_of_return > 5):
#             msg.append("恭喜，当前收益为{} ,收益率为{}".format(curr_draw,rate_of_return))
#             self.markAsNotification()
#
#         if(curr_draw < miss_point):
#             msg.append("不好，损失({}) 已抵达止损点{},请尽快处理。收益率为{}".format(curr_draw,miss_point,rate_of_return))
#             self.markAsNotification()
#
#         return "".join(msg)
#
#     #  报告
#     def reportCurrentStates(self,o):
#         states=o.getStates()
#         msg=" 最高价: {}\n 最低价：{} \n 买一价：{}\n 卖一价：{}\n 最新成交价:{} \n 成交量：{}\n 时间：{}".format(
#         states['high'],
#         states['low'],
#         states['buy'],
#         states['sell'] ,
#         states['last'],
#         states['vol'],
#         time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(states['time']))
#         )
#         return msg
