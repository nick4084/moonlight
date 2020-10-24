#!/usr/bin/python
import settings as s
import math
import time
import datetime
import requests
import json
import common
import trade
import core
import movingaverage
import history
from Objects import kline as kline_object
from Objects import order as order_object
from Indicators.rsi import RelativeStrengthIndex


class bot:

    def __init__(self, symbol, wallet, flags):
        self.symbol = symbol
        self.symbol_pair = symbol.upper() + s.trade_with
        self.wallet = wallet
        self.flags = flags
        self.state = {}
        self.value = core.getLatestBoughtPrice(self.symbol_pair)
        self.url = s.kline_endpoint + s.param_symbol_tag + self.symbol_pair + \
            s.param_interval_tag + s.trade_ticker_interval + s.param_limit_tag + '1'

    def getNewkline(self):
        '''gets the latest candle from api'''
        response = common.requests_retry_session().get(self.url)
        return kline_object.kLine(json.loads(response.text))

    def getHistoryKline(self, n=99):
        ''' gets previous number of klines from now '''
        hrs = math.ceil(n/60)
        historicalKlines = history.getHistoryPriceByStartTimestamp(sym =self.symbol_pair, interval =s.Client.KLINE_INTERVAL_1MINUTE, start = str(hrs)+' hours ago UTC')
        return historicalKlines

    def trailingProfits(self, triggerRsi, price):
        '''Take profit (sell) when trailing up condition met stragegy '''
        threshold = self.strategy['trailingProfitStrategy']['profitDropThresholdPercent']
        highestPrice = price
        currentPrice = price
        while((self.percentChange(current, highestPrice) * -1) < threshold):
            kline = self.getNewkline()
            currentPrice = float(kline.CLOSE_PRICE)
            if(currentPrice > highestPrice):
                highestPrice = currentPrice
        #when out, time to sell
        self.sellCrypto()

    # def trailingStopLoss(self):
    #     #print('trailing stop loss')
    #     return 1

    def trailingBuyLow(self, triggerRsi, price):
        '''buy when trailing down condition met against lowest RSI'''
        threshold = self.strategy['trailingBuyLowStrategy']['rsiIncreaseThreshold']
        currentRsi = triggerRsi
        lowestRsi = triggerRsi
        while(currentRsi < lowestRsi + threshold):
            kline = self.getNewkline()
            currentRsi = self.indicators['rsi14'].addKline(kline)

            if(currentRsi < lowestRsi):
                lowestRsi = currentRsi

        #when out of trailing loop, trigger buy
        self.buyCrypto()

    def buyCrypto(self):
        self.printColour('GREEN', 'BUY')
        qty = 0
        mode = ''

        if(self.flags['isPaperTrade']):
            kline = self.getNewkline()
            price = kline.CLOSE_PRICE
            mode = '[PAPER] '
            bal = self.wallet.getBalanceBySymbol(symbol=s.trade_with)
            buyQty = float(bal) / float(price)
            self.wallet.refreshBalance(symbol=self.symbol, value=buyQty)
            self.wallet.refreshBalance(symbol=s.trade_with, value=0)

        else:
            #real buy
            print('real buy')

        
        self.isLookingToBuy = False
        core.sendTelegramNotificationMessage( mode + 'BOUGHT: ' + str(buyQty) + self.symbol + ' @ ' + str(round(float(price)))+ 'USD.')

    def sellCrypto(self):
        print('SELL')
        qty = 0
        mode = ''

        if(self.flags['isPaperTrade']):
            kline = self.getNewkline()
            price = kline.CLOSE_PRICE
            mode = '[PAPER] '
            bal = self.wallet.getBalanceBySymbol(symbol=self.symbol)
            soldFor = float(bal) * float(price)
            self.wallet.refreshBalance(symbol=self.symbol, value=0)
            self.wallet.refreshBalance(symbol=s.trade_with, value=soldFor)
        else:
            print('real sell')

        self.isLookingToBuy = True
        core.sendTelegramNotificationMessage( mode + 'SOLD: ' + str(bal) + self.symbol + ' @ ' + str(round(float(price)))+ 'USD.')

    def isLossThresholdMet(self, startPrice, currentPrice, lossPercentage):
        if(startPrice == 0):
            startPrice = 1
        
        return self.percentChange(currentPrice, startPrice) <= (lossPercentage * -1)

    def percentChange(self, changedPrice, base):
        return ((float(changedPrice) / float(base)) -1 ) * 100

    def isKlineBroken(self, currentKline):
        '''if timestamp diff off by predefined threshold, will signal to restart bot by return True'''
        timeDiff = currentKline.CLOSE_TIME - self.prevKline.CLOSE_TIME
        if(timeDiff >= self.botRestartTimestampDiff_threshold):
            return True
        
        self.prevKline = currentKline
        return False

    def printColour(self, colour, text):
        print(common.textWrapper(colour, text))

    def start(self):
        '''main loop '''
        
        #####################################################
        #   Init data and strategy
        #####################################################
        # init indicators here
        klines = self.getHistoryKline(200)

        # strategy config: rsi
        self.strategy = {
            'interval' : '1m',
            'rsiPeriod' : 14,
            'buyRsiValue' : 15.5,
            'sellRsiValue' : 90,
            'trailingProfitStrategy' : {
                'profitDropThresholdPercent': 0.5
            },
            'trailingBuyLowStrategy' : {
                'rsiIncreaseThreshold': 1
            },
            'trailingstopLossStrategy' : {
                'lossThresholdPercent': 2
            }
        }

        self.indicators = {
            'rsi14' : RelativeStrengthIndex(klines, self.strategy['rsiPeriod']),
            #moving_avg : movingaverage.movingAverage(active_symbol)
        }

        self.isLookingToBuy = not self.wallet.hasBalance(self.symbol)
        self.botRestartTimestampDiff_threshold = s.milsec_in_a_min * 3
        kline = self.getNewkline()
        self.prevKline = kline
        startPrice = kline.CLOSE_PRICE

        #send noti
        state = 'buy side' if self.isLookingToBuy else 'sell side'
        mode = ' [paper] ' if self.flags['isPaperTrade'] else ''
        core.sendTelegramNotificationMessage('Starting bot ' + mode + self.symbol_pair + '...' + ' On ' + state)
        
        #####################################################
        #   Main logic
        #####################################################
        isBotActive = True
        while isBotActive:
            kline = self.getNewkline()
            # compute new indicator values
            currentRsi = self.indicators['rsi14'].addKline(kline)

            #check if kline timestamp is too far off
            if(self.isKlineBroken(currentKline=kline)):
                #restart bot
                return True
            
            print( 'buy' if self.isLookingToBuy else 'sell' + " side | RSI:"  + str(currentRsi))
            if(self.isLookingToBuy):
                # looking to buy
                if(currentRsi <= self.strategy['buyRsiValue']):
                    # trailing lower mode
                    self.trailingBuyLow(triggerRsi= currentRsi, price = kline.CLOSE_PRICE)

            else:
                # looking to sell
                if(currentRsi >= self.strategy['sellRsiValue']):
                    # trailing profits mode
                    self.trailingProfits(triggerRsi=currentRsi, price=float(kline.CLOSE_PRICE))
                elif(self.isLossThresholdMet(startPrice, float(kline.CLOSE_PRICE), self.strategy['trailingstopLossStrategy']['lossThresholdPercent'])):
                    # stop loss
                    self.sellCrypto()

            time.sleep(s.bot_delay)
# def mainLogicLoop(symbol):
#     global active_symbol
#     global bot_state
#     global value
#     global trading_currency_available
#     global my_order
#     global url
#     active_symbol = symbol
#     estimated_seconds_into_candle = 0
#     accum_vol = 0
#     curr_vol = 0

#     # determine value
#     value = core.getLatestBoughtPrice(active_symbol)
#     println('Basevalue: ' + str(value))

#     # determine available buying balance
#     trading_currency_available = core.getTradeWithQty()
#     println('buy balance available: ' + str(trading_currency_available))

#     # initialise indicator (moving average)
#     moving_avg = movingaverage.movingAverage(active_symbol)

#     # main bot loop
#     loop = True
#     while loop:
#         response = common.requests_retry_session().get(url)
#         kline = kline_object.kLine(json.loads(response.text))
#         percent_change = common.getPercentageChange(
#             float(value), float(kline.CLOSE_PRICE))

#         estimated_seconds_into_candle = common.getCandleSec(kline.OPEN_TIME)

#         ma8 = moving_avg.getCurrentSMA(kline.OPEN_TIME, kline.CLOSE_PRICE, 8)
#         ma25 = moving_avg.getCurrentSMA(kline.OPEN_TIME, kline.CLOSE_PRICE, 25)
#         ma99 = moving_avg.getCurrentSMA(kline.OPEN_TIME, kline.CLOSE_PRICE, 99)

#         #####################################################
#         # Main logic
#         #####################################################
#         if(core.is_holding_currency):
#             # has limit?
#             if(my_order == None):
#                 if(not has_limit_order()):
#                     # No limit here
#                     # TODO check limit type buy/sell
#                     # setsellLimit()
#                     print('no limit order, holding currency, setting selling limit')
#                     # delay cos weight is 5+ when no order
#                     time.sleep(s.bot_delay*3)

#             # trailing stop-loss
#             else:
#                 # have limit already placed
#                 print('trailing stop loss')
#                 trailing_stop_loss(percent_change, kline.CLOSE_PRICE)

#         else:
#             print('no holdings: inovoke buy sequence')

#         #####################################################

#         if(s.printline):
#             printResponse(kline, estimated_seconds_into_candle)
#             printMA(ma8, ma25, ma99)
#         time.sleep(s.bot_delay)


# # check for the existence of a limit order
# def has_limit_order():
#     global my_order
#     order = order_object.Order(trade.getLastOrder(active_symbol)[0])
#     if(order.has_limit_order()):
#         my_order = order
#         return True
#     else:
#         print('latest order cancelled, finding from history...')

#         orders = trade.getAllOrder(active_symbol)
#         for curr_order in orders:
#             order = order_object.Order(curr_order)
#             if(order.has_limit_order()):
#                 my_order = order
#                 return True

#     return False


# def buyIndicator():
#     print('buy indicator')


# def trailing_stop_loss(percent_change, current_price):
#     global my_order
#     global active_symbol
#     global value
#     global url

#     # trailing stop-loss
#     if(float(percent_change) < float(s.stop_loss_threshold_percent)):
#         my_order.cancelOrder()
#         my_order = None
#         # sell here to prevent further losses
#         print('sell here to prevent further losses')
#         core.sendTelegramNotificationMessage(
#             'sold to prevent loss (stoploss @' + str(s.stop_loss_threshold_percent))

#         #trade.sell_market(active_symbol, (float(my_order.ORIG_QTY) - float(my_order.EXECUTED_QTY)))

    # # trailing up profit mode
    # elif(core.is_almostreachingselltarget(float(current_price), float(my_order.PRICE))):
    #     # enter triailing mode
    #     print(common.textWrapper('WARNING', 'trailing profit mode'))
    #     target_price = float(my_order.PRICE)
    #     target_qty = float(my_order.ORIG_QTY) - float(my_order.EXECUTED_QTY)
    #     trigger_trail_price = current_price
    #     my_order.cancelOrder()
    #     my_order = None

    #     peak_price = 0
    #     while trigger_trail_price >= current_price:
    #         response = common.requests_retry_session().get(url)
    #         kline = kline_object.kLine(json.loads(response.text))
    #         percent_change = common.getPercentageChange(
    #             float(value), float(kline.CLOSE_PRICE))
    #         estimated_seconds_into_candle = common.getCandleSec(
    #             kline.OPEN_TIME)

    #         current_price = kline.CLOSE_PRICE

    #         if(current_price < trigger_trail_price):
    #             # exiting trailing mode, so add back limit order
    #             print('sell_limit back')
    #             trade.sell_limit(active_symbol, target_qty, price)
    #             my_order = order_object.Order(
    #                 trade.getLastOrder(active_symbol)[0])

    #             return

    #         elif(current_price >= target_price):
    #             # trail target_price up by defined threshold
    #             target_price = current_price
    #             if(current_price > peak_price):
    #                 peak_price = current_price
    #                 print('peak: ' + str(peak_price))
    #             else:
    #                 # if peak drops more than trailing_up_profit_stop_loss_percent, SELL
    #                 if(peak_price > current_price * ((100 + float(s.trailing_up_profit_stop_loss_percent))/100)):
    #                     print(str(peak_price) + '>' + str(current_price *
    #                                                       ((100 + float(s.trailing_up_profit_stop_loss_percent))/100)))
    #                     # SELL
    #                     print('sell here')
    #                     trade.sell_market(active_symbol, target_qty)

    #                     # cfm sell status and notify via telegram
    #                     bal = core.getAssetBalance(active_symbol)

    #                     if(bal < target_qty):
    #                         global trading_currency_available

    #                         sold_price = float(
    #                             core.getLatestSoldPrice(active_symbol))
    #                         gain = common.getPercentageChange(
    #                             float(value), sold_price)
    #                         core.sendTelegramNotificationMessage(
    #                             'sold ' + active_symbol + ' @' + str(sold_price) + ' (' + str(gain) + '%)')
    #                         value = sold_price
    #                         trading_currency_available = core.getTradeWithQty()
    #                         return
    #         elif(current_price < target_price):
    #             peak_price = 0

    #         if(s.printline):
    #             printResponse(kline, estimated_seconds_into_candle)

    #         time.sleep(s.bot_delay)


def setsellLimit():
    # set sell limit based on bought price + threshold
    global active_symbol
    bought_price = core.getLatestBoughtPrice(active_symbol)
    sell_price = core.getSellPriceByBoughtPrice(bought_price)
    sell_qty = core.getsellqty(active_symbol)
    if(sell_qty > 0):
        trade.sell_limit(active_symbol, sell_qty, sell_price)


def printResponse(kline, estimated_seconds_into_candle):
    close_price = kline.CLOSE_PRICE
    if(float(close_price) > float(kline.OPEN_PRICE)):
        line = common.textWrapper('GREEN', str(common.format2dpCurrency(close_price)) + ' (' + str(common.getPercentageChange(
            float(value), float(close_price))) + '%)' + ' vol: ' + str(kline.VOLUME) + ' ' + str(estimated_seconds_into_candle))
        println(line)
    elif(float(close_price) < float(kline.OPEN_PRICE)):
        line = common.textWrapper('RED', str(common.format2dpCurrency(close_price)) + ' (' + str(common.getPercentageChange(
            float(value), float(close_price))) + '%)' + ' vol: ' + str(kline.VOLUME) + ' ' + str(estimated_seconds_into_candle))
        println(line)
    else:
        println(str(common.format2dpCurrency(close_price)) + ' (' + str(common.getPercentageChange(float(value),
                                                                                                   float(close_price))) + '%)' + ' vol: ' + str(kline.VOLUME) + ' ' + str(estimated_seconds_into_candle))


def printMA(s, m, l):
    if(s > m > l):
        line = getMAPrintFormat('GREEN', s, m, l)
    elif(s < m < l):
        line = getMAPrintFormat('RED', s, m, l)
    else:
        line = getMAPrintFormat('WARNING', s, m, l)
    println(line)


def getMAPrintFormat(colour, s, m, l):
    return common.textWrapper(
        colour,
        'ma8: ' + str(common.format3dpCurrency(float(s))) +
        ' ma25: ' + str(common.format3dpCurrency(float(m))) +
        ' ma99: ' + str(common.format3dpCurrency(float(l))))


def println(payload):
    print(common.textWrapper('WARNING', active_symbol) + ' > ' + payload)


