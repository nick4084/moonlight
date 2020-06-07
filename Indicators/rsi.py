#!/usr/bin/python 
import numpy
import pandas as pd
from Objects import kline as kline_object

''' https://www.macroption.com/rsi-calculation/'''
class RelativeStrengthIndex:
    def __init__(self, ds, period):
        '''ds being ascending timestamp order '''
        self.closePriceInOrder = []#first item being most recent
        self.movements = []
        self.Ups = []
        self.Downs = []

        self.dataset = self.convertToList(ds)[ (len(ds) - period -1):] # period + 1 to compute movement
        self.n = period
        self.prevKline = kline_object.kLine(self.dataset[period -1])

        #get interval ms
        self.intervalMs = self.dataset[1][6] - self.dataset[0][6]

        #collect close price
        for row in self.dataset:
            self.closePriceInOrder.append(float(row[4])) #index 5 is the close price, 4 for api call
            self.nextCloseTime = row[6]
        #add 1min of ms it
        self.nextCloseTime += 60000

        self.__computeMovement()
        self.__computeUpDown()

    def convertToList(self, data):        #TODO check return list index
        if(isinstance(data, pd.DataFrame)):
            return data.values.tolist()
        return data
    
    def __computeMovement(self):
        #compute movement price from close price
        for i, closePrice in enumerate(self.closePriceInOrder):
            if(i >= 1):
                self.movements.append(closePrice - self.closePriceInOrder[i -1])
    def __computeUpDown(self):
        for change in self.movements:
            self.__addUpDown(change)

    def __getAbsAvgValue(self, arrayOfValues):
        ''' 3 method to do averaging: sma, ema, wilder smoothing method'''
        #sma
        length = len(arrayOfValues)
        if(length == 0):
            return 1
        return sum(arrayOfValues) / len(arrayOfValues)

    def __addUpDown(self, change):
        if(change <= 0):
            self.Downs.append(abs(change))
        if(change >= 0):
            self.Ups.append(abs(change))

    def __removeUpDown(self, change, last = False):
        pos = 0
        if(change <= 0):
            if(last):
                pos = len(self.Downs) -1
            self.Downs.pop(pos)
        if(change >= 0):
            if(last):
                pos = len(self.Ups) -1
            self.Ups.pop(pos)

    def __getRS(self):
        self.avgUp = self.__getAbsAvgValue(self.Ups)
        self.avgDown = self.__getAbsAvgValue(self.Downs)
        if(self.avgDown == 0 and self.avgUp == 0):
            self.printState()
            return 1

        if(self.avgDown == 0):
            self.avgDown =0.1
            self.printState()

        if(self.avgUp == 0):
            self.avgUp =0.1
            self.printState()

        return self.avgUp / self.avgDown

    def getRSI(self):
        '''return the rsi value. Ranges between 0 - 100'''
        return 100 - (100/ (1 + self.__getRS()))

    def addNewClosePrice(self, newPrice):
        '''add a new close price and remove the oldest close price 
        and re-compute RSI value
        use this funciton to add a new period to the RSI computation
        :param newPrice: the new price of last close price
        '''
        #modify the ordered close price list
        self.closePriceInOrder.pop(0)
        self.closePriceInOrder.append(float(newPrice))
        #modify the ordered movements list
        newLastMovement = float(newPrice) - float(self.closePriceInOrder[self.n -1])
        removedMovement = self.movements.pop(0)
        self.movements.append(newLastMovement)
        #modify Ups/Downs
        self.__removeUpDown(removedMovement)
        self.__addUpDown(newLastMovement)

        return self.getRSI()

    def replaceLastClosePrice(self, newPrice):
        '''replace the last close price and re-compute rsi value
        use this funciton if you want to do a 1-1 replacement of price
        :param newPrice: the new price of last close price
        '''
        newLastMovement= float(newPrice) - float(self.closePriceInOrder[self.n-1])
        #replace last close price
        self.closePriceInOrder[self.n] = float(newPrice)

        #manual replace Ups and Down
        self.__removeUpDown(self.movements[self.n-1], True)
        self.__addUpDown(newLastMovement)

        #replace last movements
        self.movements[self.n-1] = newLastMovement

        return self.getRSI()
    
    def findPriceToCriticalRsi(self, targetRsi):
        '''find the target price by changing last price to hit desired rsi value
        :param targetRsi: the desired rsi value
        '''

        targetRs = targetRsi / (100 - targetRsi)
        tempUps = self.Ups.copy()
        tempDowns = self.Downs.copy()
        #find last movement price
        lastMovement = self.movements[self.n-1]

        #remove last movement price
        if(lastMovement >= 0):
            tempUps.pop(len(tempUps)-1)
        else:
            tempDowns.pop(len(tempDowns)-1)

        #find target avgUp/avgDown
        targetAvgUp = targetRs * self.__getAbsAvgValue(tempDowns)
        targetAvgDown = self.__getAbsAvgValue(tempUps)/ targetRs

        #find target last movement
        targetLastMovementUp = targetAvgUp * (len(tempUps) + 1) - sum(tempUps)
        #print(targetLastMovementUp)
        targetLastMovementDown = targetAvgDown * (len(tempDowns) + 1) - sum(tempDowns)
        #print(targetLastMovementDown)

        #find target price
        SecondlatestPrice = self.closePriceInOrder[self.n-1]

        if(targetLastMovementUp >= 0):
            targetPrice = SecondlatestPrice + targetLastMovementUp
            #print(targetPrice)
            return targetPrice

        else :
            targetPrice = SecondlatestPrice - targetLastMovementDown
            #print(targetPrice)
            return targetPrice

    def addKline(self, kline):
        rsi = 0
        if(kline.CLOSE_TIME < self.nextCloseTime ):
            #replace
            rsi = self.replaceLastClosePrice(kline.CLOSE_PRICE)
        else:
            #add new close price
            self.nextCloseTime += self.intervalMs
            rsi = self.replaceLastClosePrice(self.prevKline.CLOSE_PRICE)
            rsi = self.addNewClosePrice(kline.CLOSE_PRICE)

        self.prevKline = kline
        return rsi


    def printState(self):
        print(self.closePriceInOrder)
        print(self.movements)
        print(self.avgUp)
        print(self.avgDown)
        print(self.Ups)
        print(self.Downs)



