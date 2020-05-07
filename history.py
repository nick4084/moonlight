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
from binance.client import Client
from Objects import kline as kline_object 
from Objects import order as order_object
import pandas as pd
import numpy as np
import time;
from datetime import date
import re

#https://medium.com/auquan/https-medium-com-auquan-machine-learning-techniques-trading-b7120cee4f05
def fetchHistory(self, flags):
    sym = flags['sym'].strip() #required
    interval = getInterval(flags['i']) #required
    if(not interval):
        print("interval invalid")
        return
    start = flags['start']#optional
    end = flags['end']#optional
    start = validateDate(start, 'start')
    end = validateDate(end, 'end')
    #row in csv, NEWER entries below
    Open_time = []
    Open= []
    High= []
    Low= []
    Close= []
    Volume= []
    Close_time= []
    Quote_asset_volume= []
    Number_of_trades= []
    Taker_buy_base_asset_volume= []
    Taker_buy_quote_asset_volume= []

    result = getHistoryPriceByDateRange(self, sym, interval, start, end)
    print(str(len(result)) + " row(s) fetched")
    #row in csv, NEWER entries below

    for row in reversed(result):
        Open_time.insert(0, row[0])
        Open.insert(0, row[1])
        High.insert(0, row[2])
        Low.insert(0, row[3])
        Close.insert(0, row[4])
        Volume.insert(0, row[5])
        Close_time.insert(0, row[6])
        Quote_asset_volume.insert(0, row[7])
        Number_of_trades.insert(0, row[8])
        Taker_buy_base_asset_volume.insert(0, row[9])
        Taker_buy_quote_asset_volume.insert(0, row[10])

    history_df = {
        'open_time' : Open_time,
        'Open' : Open,
        'High' : High,
        'Low' : Low,
        'Close' : Close,
        'Volume' : Volume,
        'Close_time' : Close_time,
        'Quote_asset_volume' : Quote_asset_volume,
        'Number_of_trades' : Number_of_trades,
        'Taker_buy_base_asset_volume' : Taker_buy_base_asset_volume,
        'Taker_buy_quote_asset_volume' : Taker_buy_quote_asset_volume
    }

    writeToCSV(history_df, start + '_to_' + end + '_' + flags['i'])




def validateDate(dtStr, name):
    #accepted format DD MMM, YYYY default: end: today, start: -1month
    if(dtStr == '-s' or dtStr == '-e'):
        return getDefaultDate(dtStr, name)
    #check date formayt is correct
    match = re.findall("(^[1-9]|[1-2][0-9]|[3][0-1])\s(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)[,]\s([0-9]{4})", dtStr)
    if(not len(match) == 1):
        print(name + 'date format is invalid')
        return getDefaultDate(dtStr, name)

    try:
        #check if date is valid
        date = datetime.datetime(int( match[0][2]), monthToMM(str(match[0][1]).upper()), int(match[0][0]))
    except:
        print(name + 'date is not a valid date')
        return getDefaultDate(dtStr, name)
    return dtStr

def getDefaultDate(dtStr, name):
    now = datetime.date.today()
    if(dtStr == '-s' or name =='start'):
        return (now + datetime.timedelta(-30)).strftime("%d %b, %Y")
    if(dtStr == '-e' or name == 'end'):
        return now.strftime("%d %b, %Y")
    
def monthToMM(MMM):
    if(MMM.upper() == 'JAN'):
        return 1
    if(MMM.upper() == 'FEB'):
        return 2
    if(MMM.upper() == 'MAR'):
        return 3
    if(MMM.upper() == 'APR'):
        return 4
    if(MMM.upper() == 'MAY'):
        return 5
    if(MMM.upper() == 'JUN'):
        return 6
    if(MMM.upper() == 'JUL'):
        return 7
    if(MMM.upper() == 'AUG'):
        return 8
    if(MMM.upper() == 'SEP'):
        return 9
    if(MMM.upper() == 'OCT'):
        return 10
    if(MMM.upper() == 'NOV'):
        return 11
    if(MMM.upper() == 'DEC'):
        return 12

def monthToMMM(MMM):
    if(MMM.upper() == 1):
        return 'JAN'
    if(MMM.upper() == 2):
        return 'FEB'
    if(MMM.upper() == 3):
        return 'MAR'
    if(MMM.upper() == 4):
        return 'APR'
    if(MMM.upper() == 5):
        return 'MAY'
    if(MMM.upper() == 6):
        return 'JUN'
    if(MMM.upper() == 7):
        return 'JUL'
    if(MMM.upper() == 8):
        return 'AUG'
    if(MMM.upper() == 9):
        return 'SEP'
    if(MMM.upper() == 10):
        return 'OCT'
    if(MMM.upper() == 11):
        return 'NOV'
    if(MMM.upper() == 12):
        return 'DEV'
    return -1

def getInterval(strInterval):

    if(strInterval == '1m'):
        return Client.KLINE_INTERVAL_1MINUTE
    if(strInterval == '3m'):
        return Client.KLINE_INTERVAL_3MINUTE
    if(strInterval == '5m'):
        return Client.KLINE_INTERVAL_5MINUTE
    if(strInterval == '15m'):
        return Client.KLINE_INTERVAL_15MINUTE
    if(strInterval == '30m'):
        return Client.KLINE_INTERVAL_30MINUTE
    if(strInterval == '1h'):
        return Client.KLINE_INTERVAL_1HOUR
    if(strInterval == '2h'):
        return Client.KLINE_INTERVAL_2HOUR
    if(strInterval == '4h'):
        return Client.KLINE_INTERVAL_4HOUR
    if(strInterval == '6h'):
        return Client.KLINE_INTERVAL_6HOUR
    if(strInterval == '8h'):
        return Client.KLINE_INTERVAL_8HOUR
    if(strInterval == '12h'):
        return Client.KLINE_INTERVAL_12HOUR
    if(strInterval == '1d'):
        return Client.KLINE_INTERVAL_1DAY
    if(strInterval == '3d'):
        return Client.KLINE_INTERVAL_3DAY
    if(strInterval == '1w'):
        return Client.KLINE_INTERVAL_1WEEK
    if(strInterval == '1mth'):
        return Client.KLINE_INTERVAL_1MONTH

    return -1              

#history kline

def getHistoryPrice(sym, start_ms, interval = Client.KLINE_INTERVAL_1MINUTE):
    result = s.client.get_historical_klines(
        symbol = sym,
        interval = interval, 
        start_str = str(start_ms),
        limit = 1000)

    return result

def getHistoryPriceByRange(sym, start_ms, end_ms, interval = Client.KLINE_INTERVAL_1MINUTE):
    result = s.client.get_historical_klines(
        symbol = sym,
        interval = interval, 
        start_str = str(start_ms),
        end_str = str(end_ms),
        limit = 1000)

    return result

def getHistoryPriceByDateRange(self, sym, interval, start, end, limit = 1000):
    return s.client.get_historical_klines(
        symbol = sym,
        interval = interval, 
        start_str = str(start),
        end_str = str(end),
        limit = 1000)

def writeToCSV(df, fileName):
    df = pd.DataFrame(df)

    df.to_csv('./data/' + fileName + '.csv')

