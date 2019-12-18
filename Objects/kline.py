#!/usr/bin/python
import datetime

class kLine:
    def __init__(self, kline_arr):
        if(len(kline_arr) == 1):
            self.kline = kline_arr[0]
        else:
            self.kline = kline_arr
        self.OPEN_TIME = self.kline[0]
        self.OPEN_DT = datetime.datetime.fromtimestamp(self.OPEN_TIME/1000.0)
        self.OPEN_PRICE = self.kline[1]
        self.HIGH_PRICE = self.kline[2]
        self.LOW_PRICE = self.kline[3]
        self.CLOSE_PRICE = self.kline[4] #also latest price
        self.VOLUME = self.kline[5]
        self.CLOSE_TIME = self.kline[6]
        self.CLOSE_DT = datetime.datetime.fromtimestamp(self.CLOSE_TIME/1000.0)
        self.QUOTE_ASSET_VOLUME = self.kline[7]
        self.NUM_OF_TRADE = self.kline[8]
        self.TAKER_BUY_BASE_ASSET_VOLUME = self.kline[9]
        self.TAKER_BUY_QUOTE_ASSET_VOLUME = self.kline[10]
        self.IGNORE = self.kline[11]