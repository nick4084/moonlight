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
import pandas as pd
import numpy as np

import time;
#https://medium.com/auquan/https-medium-com-auquan-machine-learning-techniques-trading-b7120cee4f05
def collect(sym):
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


    startarray = ["1 Dec, 2017", "1 Jan, 2018"]
    endarray = []
    ts = time.time()
    collect = True
    latest_close_time = 0
    result = trade.getHistoryPrice(sym, "16 hours ago UTC")
    for row in result:
        Open_time.append(row[0])
        Open.append(row[1])
        High.append(row[2])
        Low.append(row[3])
        Close.append(row[4])
        Volume.append(row[5])
        Close_time.append(row[6])
        Quote_asset_volume.append(row[7])
        Number_of_trades.append(row[8])
        Taker_buy_base_asset_volume.append(row[9])
        Taker_buy_quote_asset_volume.append(row[10])

    latest_close_time = Close_time[0]
    
    #NEWER entries at the end
    range_of_timestamp  = 60000000 - 60000
    latest_close_time = int(latest_close_time) + 1
    end_close_time =latest_close_time - range_of_timestamp
    for i in range(0, 10):
        result = trade.getHistoryPriceByRange(sym,str(end_close_time), str(latest_close_time))
        print(str(len(result)))
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

        latest_close_time = Close_time[0]
        latest_close_time = int(latest_close_time) + 1
        end_close_time = latest_close_time - range_of_timestamp

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

    df = pd.DataFrame(history_df)

    df.to_csv('/data/' + str(ts) + '_to_' + str(latest_close_time) + '.csv')


