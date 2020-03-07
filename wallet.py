#!/usr/bin/python
import settings
import core
from paperbalance import assets

#This script hold the wallet balance and some access functions



ASSET = "asset"
FREE = "free"
LOCKED = "locked"
balance = {}

def init():
    global balance
    balance = {}

    if "p" in settings.flags:
        __paperWallet()
    else:
        __actualWallet()

def __paperWallet():
    #init paper wallet
    global balance
    print("initializing paper wallet from file... ")
    balance = assets

def __actualWallet():
    #init actual wallet
    global balance
    print("loading wallet balance from " + settings.source + "... ")
    balance = core.fetchAccBalance()

def getAllBalance():
    global balance
    return balance


def getBalanceBySymbol(sym):
    global balance
    sym = sym.upper()
    print(sym)
    for bal in balance:
        if(bal.get(ASSET) == sym):
            print(bal.get(FREE))

def refreshActual():
    global balance
    balance = core.fetchAccBalance()

def savePaperBalance():
    global balance
    
