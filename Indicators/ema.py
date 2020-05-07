#!/usr/bin/python 
import numpy
from Objects import kline as kline_object
from sma import simpleMovingAverage
closePriceList = [] #first item being most recent
''' after init, it does not have a ema value as the initial ds is used to determine timeperiod
Simply add another kline to generate a ema value by calling addKlineAndGetEMA()'''
class exponentialMovingAverage:
    def __init__(self, ds):
        #ema = (closeprice - ema(previous day) * multiplier + ema(previous day))
        #initial ema is computed with sma instead
        global n
        global emaValue
        global weight
        global latestClosePrice
        n = len(ds)
        weight = self.getWeightedMultiplier(n)
        latestClosePrice = kline_object.kLine(ds.pop()).CLOSE_PRICE
        emaValue = sma = simpleMovingAverage(ds).getSMA()
        #use sma to compute ema for next point
        emaValue = self.computeEMA()



    def getWeightedMultiplier(timePeriod):
        return 2/(timePeriod +1)

    def computeEMA(newClosePrice):
        global latestClosePrice, emaValue, weight
        return (latestClosePrice - emaValue)  * weight + emaValue



    def addKlineAndGetEMA(newKline):
        global emaValue, latestClosePrice
        
        kline = kline_object.kLine(newKline)
        
        newClosePrice = kline.CLOSE_PRICE
        emaValue = self.computeEMA(newClosePrice)
        latestClosePrice = newClosePrice

        return emaValue


        

