#!/usr/bin/python 
import numpy
from Objects import kline as kline_object

closePriceList = [] #first item being most recent

class simpleMovingAverage:
    def __init__(self, ds):
        global n
        global closePriceList
        global smaValue
        n = len(ds)
        closePriceList = self.extractClosePriceInOrder(ds, n)
        smaValue = self.computeSMA()

    def addKline(newKline):
        global smaValue, n, closePriceList
        #remove old value, add new
        kline = kline_object.kLine(newKline)
        
        valueToRemove = float(closePriceList.pop(n-1))
        closePriceList.insert(float((kline.CLOSE_PRICE))
        newSummation = (smaValue * n) -valueToRemove + float(kline.CLOSE_PRICE)
        smaValue = newSummation / n

        return smaValue

    def computeSMA():
        global closePriceList, smaValue, n
        smaValue = sum(closePriceList)/ n
        return smaValue

    def extractClosePriceInOrder(ds, n):
        orderedClosePriceList = []
        indexkline = kline_object.kLine(ds[0])
        lastKline = kline_object.kLine(n-1)

        if(indexkline.OPEN_DT < lastKline.OPEN_DT):
            #last item being latest need to reverse order
            ds = reversed(ds)

        for candle in ds:
            kline = kline_object.kLine(candle)
            orderedClosePriceList.append(float(kline.CLOSE_PRICE))
        
        return orderedClosePriceList


        

