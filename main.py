#!/usr/bin/python
import configparser

from binance.enums import *
from binance.websockets import BinanceSocketManager
from bot import bot
from key import *
import json
import settings
import history
import sys
from wallet import Wallet

PARM_IS_PAPER_TRADE = "isPaperTrade"
PARAM_IS_OBSERVE_ONLY = "isObserveOnly"
PARAM_CONFIG_FILENAME = "configFileName"
PARAM_CONFIG_KEY = "TRADING_CONFIG"
PARAM_CONFIG_PAPER_WALLET = "PAPER_WALLET_CONFIG"

# default args
flags = {
    PARM_IS_PAPER_TRADE: False,
    PARAM_IS_OBSERVE_ONLY: False,
    PARAM_CONFIG_FILENAME: 'btc'
}


# interpret flags
#sample: python3 main.py -p -c btc
for (i, arg) in enumerate(sys.argv):

    if(arg.startswith('-')):
        #read single flag
        if arg == '-p':
            flags[PARM_IS_PAPER_TRADE] = True
            continue

        if arg == '-o':
            flags[PARAM_IS_OBSERVE_ONLY] = True
            continue

        if(i < len(sys.argv) - 1):
            #read flags that takes input (cannot be last item in argv)
            if arg == '-c':
                flags[PARAM_CONFIG_FILENAME] = sys.argv[i + 1]
                continue


start = True
while(start):
    # Initialise requirements
    settings.init(flags)

    # read trading config
    config = configparser.RawConfigParser()
    config.read('./TradingConfig/'+ flags[PARAM_CONFIG_FILENAME] +'.txt')
    tradingConfig = dict(config.items(PARAM_CONFIG_KEY))
    walletConfig = dict(config.items(PARAM_CONFIG_PAPER_WALLET))
    paperWallet = walletConfig['balance']
    jsonWallet = json.loads(paperWallet)

    #init wallet
    wallet = Wallet(flags[PARM_IS_PAPER_TRADE], jsonWallet)


    #bot 
    btcBot = bot(symbol=flags[PARAM_CONFIG_FILENAME], wallet=wallet, flags=flags)

    print("Start.")
    start = btcBot.start()
