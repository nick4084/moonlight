#!/usr/bin/python
from binance.enums import *
from binance.websockets import BinanceSocketManager
from key import *
import settings
import bot
import history


#Initialise requirements
settings.init()

balances = settings.account_balance
for asset in balances:
    if(asset['asset'] != settings.trade_with):
        print(asset['asset'] + settings.trade_with)
    else:
        print(asset)
#bot.monitor('BNBUSDT')

history.collect('BCHABCUSDT')