#!/usr/bin/python
from binance.enums import *
from binance.websockets import BinanceSocketManager
from key import *
import settings
import bot
import history
import sys
import wallet



#interpret flags
flags = {}
for arg in sys.argv:

    if arg == '-p' :
        flags["p"] =  "paper"
        continue

    if arg == '-o':
        flags["o"] =  "observe"
        continue


#Initialise requirements
settings.init(flags)
wallet.init()
wallet.getBalanceBySymbol("bnb")
