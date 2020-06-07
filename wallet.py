#!/usr/bin/python
import settings
import core
from paperbalance import assets

# This script hold the wallet balance and some access functions
minBalanceToConsideredActive = 0.001
ASSET = "asset"
FREE = "free"
LOCKED = "locked"
balance = {}

#eg of wallet format
# [
#     {'asset': 'BNB', 'free': '1.17801202', 'locked': '0.00000000'}, 
#     {'asset': 'USDT', 'free': '0.00134803', 'locked': '0.00000000'}, 
#     {'asset': 'BCHABC', 'free': '5.99054032', 'locked': '0.00000000'}, 
#     {'asset': 'BCH', 'free': '5.99054032', 'locked': '0.00000000'}
#  ]

class Wallet:

    def __init__(self, isPaperWallet, balance={}):
        self.isPaperWallet = isPaperWallet
        if isPaperWallet:
            print("initializing paper wallet... ")
            self.balance = balance
            print(self.balance)
        else:
            print("loading wallet balance from " + settings.source + "... ")
            self.balance = core.fetchAccBalance()


    def getAllBalance(self):
        return self.balance


    def getBalanceBySymbol(self, symbol):
        sym = symbol.upper()
        for bal in self.balance:
            if(bal.get(ASSET) == sym):
                return bal.get(FREE)

    def refreshBalance(self):
        """refrest actual wallet balance"""
        self.balance = core.fetchAccBalance()

    def refreshBalance(self, symbol, value):
        """update paper wallet balance"""
        print(self.balance)
        for i ,bal in enumerate(self.balance):
            if(bal.get(ASSET) == symbol):
                self.balance[i][FREE] = value
        
        print(self.balance)
        
    def hasBalance(self, symbol):
        sym = symbol.upper()
        for bal in self.balance:
            if(bal.get(ASSET) == sym and float(bal.get(FREE)) >= minBalanceToConsideredActive):
                return True
            
        return False
