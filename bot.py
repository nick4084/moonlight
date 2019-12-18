#!/usr/bin/python
import settings as s
import time
import datetime
import requests
import json
import common
import trade
import core
import movingaverage
from Objects import kline as kline_object 
from Objects import order as order_object

state_looking_to_sell = 'SELLING_STATE'
state_looking_to_buy = 'BUYING_STATE'

value = 400
active_symbol = ''
bot_state = ''
trading_currency_available = 0
my_order = None
url = ''


def monitor(symbol):
    global active_symbol 
    global bot_state
    global value
    global trading_currency_available
    global my_order
    global url
    url = s.kline_endpoint+ s.param_symbol_tag + symbol + s.param_interval_tag + s.trade_ticker_interval + s.param_limit_tag + '1'
    active_symbol = symbol
    estimated_seconds_into_candle = 0
    accum_vol = 0
    curr_vol = 0

    #determine value
    value = core.getLatestBoughtPrice(active_symbol)
    println('Basevalue: '+ str(value))

    #determine available buying balance 
    trading_currency_available = core.getTradeWithQty()
    println('buy balance available: '+ str(trading_currency_available))

    #initialise indicator (moving average)
    moving_avg = movingaverage.movingAverage(active_symbol)

    #main bot loop
    loop = True
    while loop:
        response = common.requests_retry_session().get(url)
        kline = kline_object.kLine(json.loads(response.text))
        percent_change = common.getPercentageChange(float(value), float(kline.CLOSE_PRICE))

        estimated_seconds_into_candle = common.getCandleSec(kline.OPEN_TIME)

        ma8 = moving_avg.getCurrentSMA(kline.OPEN_TIME, kline.CLOSE_PRICE, 8)
        ma25 = moving_avg.getCurrentSMA(kline.OPEN_TIME, kline.CLOSE_PRICE, 25)
        ma99 = moving_avg.getCurrentSMA(kline.OPEN_TIME, kline.CLOSE_PRICE, 99)

        #####################################################
        # Main logic
        #####################################################
        if(core.is_holding_currency):
            #has limit?
            if(my_order == None):
                if(not has_limit_order()):
                    #No limit here
                    #TODO check limit type buy/sell
                    #setsellLimit()
                    print('no limit order, holding currency, setting selling limit')
                    #delay cos weight is 5+ when no order
                    time.sleep(s.bot_delay*3)

                
            #trailing stop-loss
            else:
                #have limit already placed
                print('trailing stop loss')
                trailing_stop_loss(percent_change, kline.CLOSE_PRICE)

        else:
            print('no holdings: inovoke buy sequence')



        #####################################################

        if(s.printline):
            printResponse(kline, estimated_seconds_into_candle)
            printMA(ma8, ma25, ma99)
        time.sleep(s.bot_delay)
        

#check for the existence of a limit order
def has_limit_order():
    global my_order
    order = order_object.Order( trade.getLastOrder(active_symbol)[0] )
    if(order.has_limit_order()):
        my_order = order
        return True
    else:
        print('latest order cancelled, finding from history...')
        
        orders = trade.getAllOrder(active_symbol)
        for curr_order in orders:
            order = order_object.Order(curr_order)
            if(order.has_limit_order()):
                my_order = order
                return True
    
    return False

def buyIndicator():
    print('buy indicator')

def trailing_stop_loss(percent_change, current_price):
    global my_order
    global active_symbol
    global value
    global url

    #trailing stop-loss
    if(float(percent_change) < float(s.stop_loss_threshold_percent)):
        my_order.cancelOrder()
        my_order = None
        #sell here to prevent further losses
        print('sell here to prevent further losses')
        core.sendTelegramNotificationMessage('sold to prevent loss (stoploss @' + str(s.stop_loss_threshold_percent) )

        #trade.sell_market(active_symbol, (float(my_order.ORIG_QTY) - float(my_order.EXECUTED_QTY)))
        
    #trailing up profit mode
    elif(core.is_almostreachingselltarget(float(current_price), float(my_order.PRICE))):
        #enter triailing mode
        print(common.textWrapper('WARNING', 'trailing profit mode'))
        target_price = float(my_order.PRICE)
        target_qty = float(my_order.ORIG_QTY) - float(my_order.EXECUTED_QTY)
        trigger_trail_price = current_price
        my_order.cancelOrder()
        my_order = None

        peak_price = 0
        while trigger_trail_price >= current_price:
            response = common.requests_retry_session().get(url)
            kline = kline_object.kLine(json.loads(response.text))
            percent_change = common.getPercentageChange(float(value), float(kline.CLOSE_PRICE))
            estimated_seconds_into_candle = common.getCandleSec(kline.OPEN_TIME)

            current_price = kline.CLOSE_PRICE

            if(current_price < trigger_trail_price):
                #exiting trailing mode, so add back limit order
                print('sell_limit back')
                trade.sell_limit(active_symbol, target_qty, price)
                my_order = order_object.Order( trade.getLastOrder(active_symbol)[0] )

                return

            elif(current_price >= target_price ):
                #trail target_price up by defined threshold
                target_price = current_price 
                if(current_price > peak_price):
                    peak_price = current_price
                    print('peak: ' + str(peak_price))
                else:
                    #if peak drops more than trailing_up_profit_stop_loss_percent, SELL
                    if( peak_price > current_price * ((100 + float(s.trailing_up_profit_stop_loss_percent))/100) ):
                        print(str(peak_price) + '>' + str(current_price * ((100 + float(s.trailing_up_profit_stop_loss_percent))/100)))
                        #SELL
                        print('sell here')
                        trade.sell_market(active_symbol, target_qty)

                        #cfm sell status and notify via telegram
                        bal = core.getAssetBalance(active_symbol)

                        if(bal < target_qty):
                            global trading_currency_available

                            sold_price = float(core.getLatestSoldPrice(active_symbol))
                            gain = common.getPercentageChange(float(value), sold_price)
                            core.sendTelegramNotificationMessage('sold ' + active_symbol + ' @' + str(sold_price) + ' (' + str(gain) + '%)')
                            value = sold_price
                            trading_currency_available = core.getTradeWithQty()
                            return
            elif(current_price < target_price):
                peak_price = 0

            if(s.printline):
                printResponse(kline, estimated_seconds_into_candle)
            
            time.sleep(s.bot_delay)





def setsellLimit():
    #set sell limit based on bought price + threshold
    global active_symbol
    bought_price = core.getLatestBoughtPrice(active_symbol)
    sell_price = core.getSellPriceByBoughtPrice(bought_price)
    sell_qty = core.getsellqty(active_symbol)
    if(sell_qty > 0):
        trade.sell_limit(active_symbol, sell_qty, sell_price)





def printResponse(kline, estimated_seconds_into_candle):
    close_price = kline.CLOSE_PRICE
    if(float(close_price) > float(kline.OPEN_PRICE)):
        line = common.textWrapper('GREEN', str(common.format2dpCurrency(close_price)) + ' (' +str(common.getPercentageChange(float(value), float(close_price))) +'%)'+ ' vol: '+ str(kline.VOLUME) + ' ' + str(estimated_seconds_into_candle))
        println(line)
    elif(float(close_price) < float(kline.OPEN_PRICE)):
        line = common.textWrapper('RED', str(common.format2dpCurrency(close_price)) + ' (' +str(common.getPercentageChange(float(value), float(close_price))) +'%)'+ ' vol: '+ str(kline.VOLUME) + ' ' + str(estimated_seconds_into_candle))
        println(line)
    else:
        println(str(common.format2dpCurrency(close_price)) + ' (' +str(common.getPercentageChange(float(value), float(close_price))) +'%)'+ ' vol: '+ str(kline.VOLUME) + ' ' + str(estimated_seconds_into_candle))

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
    ' ma99: ' + str(common.format3dpCurrency(float(l))) )

def println(payload):
    print(common.textWrapper('WARNING', active_symbol) + ' > ' + payload)



    