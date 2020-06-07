#!/usr/bin/python 
import numpy
from Objects import kline as kline_object
from .ema import exponentialMovingAverage

''' require dataset to be at least of length longEmaPeriod + signalPeroid eg. 26 + 9 = len 35
    to get first signal point, call addClosePrice() 
'''
class macd:
    def __init__(self, dataset, shortEmaPeriod = 12, longEmaPeriod = 26 ,signalPeriod = 9):
        self.macdList = [] #first item being oldest
        self.shortPeriod = shortEmaPeriod
        self.longPeroid = longEmaPeriod
        self.signalPeriod = signalPeriod
        self.dataset = dataset
        
        self.shortEma = exponentialMovingAverage(dataset[(longEmaPeriod - shortEmaPeriod):longEmaPeriod -1]) #(longPeriod - shortPeriod) to longperiod
        self.longEma = exponentialMovingAverage(dataset[0:longEmaPeriod -1]) # 0 to longperiod -1

        self.initSignal()


    def initSignal(self):
        ''' generate enough macd value for the first signal '''
        
        for i in range(0, self.signalPeriod -1):
            closePrice = self.dataset[self.longEmaPeriod + i] # index start from after longPeriod
            shortEmaVal = self.shortEma.addClosePriceAndGetEMA(closePrice)
            longEmaVal = self.longEma.addClosePriceAndGetEMA(closePrice)
            self.macd.append(shortEmaVal - longEmaVal)

        if(len(self.macd) >= self.signalPeriod):
            self.signalEma = exponentialMovingAverage(macd)

    def addClosePrice(self, closePrice):
        emaShort = self.shortEma.addClosePriceAndGetEMA(closePrice)
        emaLong = self.longEma.addClosePriceAndGetEMA(closePrice)
        signalValue = emaShort - emaLong        
        self.macd = self.macd[1:]
        self.macd.append(signalValue)
        signal = self.signalEma.addClosePriceAndGetEMA(signalValue)
        
        return [emaShort, emaLong, emaSignal]


        

