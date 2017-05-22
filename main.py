#!/usr/bin/python
#-*- coding:utf-8 -*-

import time
import sys
import requests



from watchdog import WatchDog
from strategy import DogStrategy
from trander import Trander


requests.adapters.DEFAULT_RETRIES = 15

if __name__=="__main__":


    while(True):
        strategy=DogStrategy()

        s=WatchDog().watching("doge",strategy)
        t=Trander()
        my=t.balance()
        # my_money=float(my['cny_balance'])
        if s.isBuy():
            sys.stdout.write("+")
            # can_buy_nu=int(my_money/s.price)
            # s.setNu(can_buy_nu)
            data=t.buy(s)
            if(data['result']):
                print("自动在价格{}处买入{} 个狗狗币 ".format(s.price,s.nu))
                strategy.set_curr_keep_price(['doge',s.nu,s.price,int(time.time())])
                print(data)

        elif s.isSell():
            sys.stdout.write("-")
            data=t.sell(s)
            print("即将 自动在价位{}卖出数量{} 个狗狗币，预计 赚 {} RMB".format(s.price,s.nu,s.money))

            if(data['result']):
                print("自动在价位{}卖出数量{} 个狗狗币，赚了 {} RMB".format(s.price,s.nu,s.money))
                strategy.set_curr_keep_price_empty()

        else:
            sys.stdout.write(".")
        sys.stdout.flush()
        time.sleep(5)
