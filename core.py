#!/usr/bin/python
import settings
import requests
import common
import json
import trade

def fetchAccBalance():
    balance = settings.client.get_account()
    balances = balance['balances']
    acct_bal = []
    for currency in balances:
        if(float(currency['free'])> 0.00001 or float(currency['locked'])>0.00001):
            acct_bal.append(currency)
        
    return acct_bal

def getTradeWithQty():
    fetchAccBalance()
    return getAssetBalance(settings.trade_with)

def getAssetBalance(currency):
    balances = settings.account_balance
    for balance in balances:
        if(balance['asset'] == currency):
            return float(balance['free'])
    return 0

def is_holding_currency(currency):
    balances = settings.account_balance
    for balance in balances:
        if(balance['asset'] == currency):
            if(float(balance['free']) > 0.0001):
                return True
            else:
                return False
    print('Not holding any of ' + str(currency))
    return False

#Return a price value. Either last purchase value or last sell value.
#Return -1 otherwise
def getAssetBaseValue(sym):
    orders = trade.getAllOrder(sym)
    for order in reversed(orders):
        if(order != None):
            if(order['status'] == 'FILLED'):
                return float(order['price'])
    return -1

def getLatestBoughtPrice(sym):
    results = trade.getMyTrades(sym)
    for trade_entry in reversed(results):
        if(trade_entry['isBuyer']):
            return trade_entry['price']

def getLatestSoldPrice(sym):
    results = trade.getMyTrades(sym)
    for trade_entry in reversed(results):
        if(not trade_entry['isBuyer']):
            return trade_entry['price']

#if 80% of target is met
def is_almostreachingselltarget(currentprice, targetprice):
    if(float(currentprice) >= (float(targetprice)/ ( 100 + (float(settings.profit_threshold_percent) * 0.1 ))*100) ):
        print('Trail mode target: ' + str(float(targetprice)/ ( 100 + (float(settings.profit_threshold_percent) * 0.1 ))*100) )
        return True
    else:
        print('Trail mode target: ' + str(float(targetprice)/ ( 100 + (float(settings.profit_threshold_percent) * 0.1 ))*100) )
        return False

#return selling price with profit markup from threshold
def getSellPriceByBoughtPrice(bought_price):
    return float(bought_price) * (100 + float(s.profit_threshold_percent))*0.01

def getsellqty(sym):
    fetchAccBalance()
    balance = getAssetBalance(sym)
    if(sym == 'BNB'):
        balance = balance - settings.min_bnb_holding
        if(balance < 0):
            balance = 0
    return balance

def getAssetmarketValue(sym):
    url = settings.price_ticker_endpoint + settings.param_symbol_tag + sym
    response = requests.get(url) #{"symbol":"BTCUSDT","price":"7816.00000000"}
    response_json = json.loads(response.text)
    return float(response_json['price'])

def sendTelegramNotificationMessage(message):
    url = settings.telegram_api_endpoint + settings.telegram_api_key + settings.method_telegram_sendmessage + settings.param_telegram_chat_id + '&' + settings.param_telegram_message + message

    common.requests_retry_session().get(url)
