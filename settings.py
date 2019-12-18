#!/usr/bin/python
from key import *
import core
from binance.client import Client
#This file declare and hold global variable across program

def init():
    #############IMPORTANT############
    global is_test_mode
    is_test_mode = False
    #################################
    global client 
    client = key().getClient()
    global account_balance # eg. {'asset': 'BTC', 'free': '0.15554411', 'locked': '0.00000000'}
    account_balance = []
    core.fetchAccBalance()

    #portfolio
    global portfolio
    portfolio = { 'BTC': 0.4, 'BCHABC': 0.4, 'ETH': 0.2 }


    #URL declaration
    global kline_endpoint 
    global trade_endpoint
    global trade_test_endpoint
    global price_ticker_endpoint
    global param_symbol_tag
    global param_interval_tag
    global param_limit_tag

    base_endpoint = 'https://api.binance.com'
    kline_endpoint = base_endpoint + '/api/v1/klines?'
    trade_endpoint = base_endpoint + '/api/v3/order?'
    trade_test_endpoint = base_endpoint + '/api/v3/order/test?'
    price_ticker_endpoint = base_endpoint + '/api/v3/ticker/price?'
    param_symbol_tag = '&symbol='
    param_interval_tag = '&interval='
    param_limit_tag = '&limit='

    #price settings
    global profit_threshold_percent
    global stop_loss_threshold_percent
    global trailing_buy_threshold_percent
    global trailing_up_profit_stop_loss_percent
    global buy_low_threshold_percent
    global trade_with #'fiat'
    global trade_ticker_interval
    global min_bnb_holding


    profit_threshold_percent = 1.200
    stop_loss_threshold_percent = -1.000
    trailing_up_profit_stop_loss_percent = 0.3
    buy_low_threshold_percent = 0.1
    trailing_buy_threshold_percent = 0.3
    min_bnb_holding = 1
    trade_with = 'USDT'
    trade_ticker_interval = Client.KLINE_INTERVAL_1MINUTE



    #general settings
    global printline
    global bot_delay
    global milsec_in_a_min

    bot_delay = 1.0 #approx 1~2/sec
    printline = True
    milsec_in_a_min = 60000

    #telegram bot settings
    global telegram_api_key
    global telegram_bot_username
    global telegram_firstname
    global telegram_api_endpoint
    global telegram_chat_id
    global method_telegram_sendmessage
    global param_telegram_chat_id
    global param_telegram_message

    telegram_api_key = '832263699:AAEbl8cenDp1pWdwWX5Bsv-36KjbQVvUBvM'
    telegram_bot_username = 'trading_bot4084_bot'
    telegram_firstname = 'trade transaction'
    telegram_api_endpoint = 'https://api.telegram.org/bot'
    telegram_chat_id = '330817807'
    method_telegram_sendmessage = '/sendmessage?'
    param_telegram_chat_id = 'chat_id=' + telegram_chat_id
    param_telegram_message = 'text='




