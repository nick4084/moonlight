import pandas as pd
from Indicators.rsi import RelativeStrengthIndex as rsi
import matplotlib.pyplot as plt
import numpy as np


class strategyRsi: 

    def __init__(self, klines, buyFunc, sellFunc, rsiPeriod =14, buyRsiValue=15.5, sellRsiValue=90):
        #init values
        self.period = rsiPeriod
        self.sellRsiValue = sellRsiValue
        self.buyRsiValue = buyRsiValue
        rsi14 = rsi(klines, rsiPeriod)

    def feed(self, isBuying, openPrice, highPrice, lowPrice, closePrice):
        if(self.isPriceSameAsPrev(openPrice, highPrice, lowPrice, closePrice)):
            return None

        newRsiValue = self.rsi14.addNewClosePrice(closePrice)

        if(isBuying):
            if(newRsiValue <= targetPrice):
                #signal to buy. 
                    btc += buy(targetPrice, usd)
                    usd = 0
                    lastBuyPrice = targetPrice
                    print('buy '+ str(btc) +' at '+ str(targetPrice))
                    print('bal: ', btc)
                    buyx.append(i)
                    buyy.append(targetPrice)
                    isLookingToBuy = False
            
            else:
                #looking to sell
                targetPrice = rsi14.findPriceToCriticalRsi(sellRsiValue)
                if( hp >= targetPrice):
                    #buy at target price
                    print('sell '+ str(btc) +' at '+ str(targetPrice))
                    usd += sell(targetPrice, btc)
                    btc = 0
                    print('bal: ', usd)
                    sellx.append(i)
                    selly.append(targetPrice)
                    pnlValue = pnl(lastBuyPrice, targetPrice)
                    if(pnlValue > 0 ):
                        win += 1

        
    
    def isPriceSameAsPrev(self, openPrice, highPrice, lowPrice, closePrice):
        #return if kline same as prev
        if(openPrice == self.lastOpenPrice and highPrice == self.lasthighPrice and 
        lowPrice == self.lastlowPrice and closePrice == self.lastclosePrice){
            return True
        }
        #update last price
        self.updateLastPrice(openPrice, highPrice, lowPrice, closePrice)
        return False

    def updateLastPrice(self, openPrice, highPrice, lowPrice, closePrice):
        self.openPrice = openPrice
        self.highPrice = highPrice
        self.lowPrice = lowPrice
        self.closePrice = closePrice

def Strategy(period, sellRsiValue, buyRsiValue):
    global klines, totalComms, tradeExpenses, gridSearch

    rsi14 = rsi(klines, period)
    rsiList = []
    xAxis = []
    i = period -1
    rsiList.append(rsi14.getRSI())

    xAxis.append(period+1)
    for index, row in klines.iterrows():
        if(index == period+1):
            startprice = float(row[5])
        if(index == i):
            cp = float(row[5]) #index 5 is the close price
            hp = float(row[3]) #index 3 is the high price
            lp = float(row[4]) #index 4 is the low price
            op = float(row[2]) #index 4 is the low price
            
            endprice = cp
            if(cp == hp and hp == lp and lp == op):
                continue



            newRsiValue = rsi14.addNewClosePrice(cp)
            rsiList.append(newRsiValue)
            xAxis.append(i)

            if(isLookingToBuy):
                targetPrice = rsi14.findPriceToCriticalRsi(buyRsiValue)
                if(lp <= targetPrice):
                    #buy at target price
                    btc += buy(targetPrice, usd)
                    usd = 0
                    lastBuyPrice = targetPrice
                    print('buy '+ str(btc) +' at '+ str(targetPrice))
                    print('bal: ', btc)
                    buyx.append(i)
                    buyy.append(targetPrice)
                    isLookingToBuy = False
            
            else:
                #looking to sell
                targetPrice = rsi14.findPriceToCriticalRsi(sellRsiValue)
                if( hp >= targetPrice):
                    #buy at target price
                    print('sell '+ str(btc) +' at '+ str(targetPrice))
                    usd += sell(targetPrice, btc)
                    btc = 0
                    print('bal: ', usd)
                    sellx.append(i)
                    selly.append(targetPrice)
                    pnlValue = pnl(lastBuyPrice, targetPrice)
                    if(pnlValue > 0 ):
                        win += 1
                    else :
                        loss +=1
                    
                    print('     p/l', pnlValue)
                    print('  ')

                    isLookingToBuy = True
            i+=1
    print(' ')
    print('############## SUMMARY ################')
    if(btc > 0):
        usd = sell(lastBuyPrice, btc)
        print('btc~ ', round(usd, 2))
    print('strategy pnl:{0} % |  market performace: {1} %'.format(round(pnl(1000, usd), 2), round(pnl(startprice, endprice), 2)))
    print('win: {0} loss: {1} | commission expense: {2} USD'.format(win, loss, round(totalComms, 2)))
    gridSearch.append({'period': period, 'buyrsi': buyRsiValue, 'sellrsi': sellRsiValue, 'pnl' : round(pnl(1000, usd), 2), 'market performance' :  round(pnl(startprice, endprice), 2), 'stats': 'win: {0} loss: {1} | commission expense: {2} USD'.format(win, loss, round(totalComms, 2))})
    
    # fig, ax = plt.subplots()  # Create a figure containing a single axes.
    # ax.plot(xAxis, rsiList)  # Plot some data on the axes.
    # ax.plot([0, i], [sellRsiValue, sellRsiValue])
    # ax.plot([0, i], [buyRsiValue, buyRsiValue])
    # plt.show()

    # fig1, ax1 = plt.subplots()
    # ax1.scatter(buyx, buyy, marker="P")
    # ax1.scatter(sellx, selly, marker="X")


gridSellRsi = [75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90]
gridBuyRsi= [14.5, 15, 15.5, 16, 17.5, 18, 18.5, 19, 19.5, 20, 20.5, 21, 21.5, 22, 22.5, 23]


#gridSellRsi = [90]
#gridBuyRsi= [14.5]

for buyRsi in gridBuyRsi:
    for sellRsi in gridSellRsi:
        Strategy(14, sellRsi, buyRsi)

print(gridSearch)

#find best pair
highest = 0
highestDetails = 0
for result in gridSearch:
    print(result)
    if(result['pnl'] > highest):
        highest = result['pnl']
        highestDetails = result

print(highest)
print(highestDetails)