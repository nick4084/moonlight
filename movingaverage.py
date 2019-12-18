#!/usr/bin/python 

import settings
import common
import json
import numpy
from Objects import kline as kline_object

dataset = [] #first item being most recent
active_symbol = ''
latest_milisec = 0
oldest_milisec = 0
ma_cache = {}
window_last_added_latest_close_price = {}
class movingAverage:
    def __init__(self, symbol, dataset_count = 100):
        global active_symbol
        global ds_count
        active_symbol = symbol
        ds_count = dataset_count
        dataset = self.fetchdataset(symbol, dataset_count)

    def fetchdataset(self, symbol, count):
        global dataset
        global latest_milisec
        global oldest_milisec
        dataset.clear()
        url = settings.kline_endpoint+ settings.param_symbol_tag + symbol + settings.param_interval_tag + settings.trade_ticker_interval + settings.param_limit_tag + str(count)
        response = common.requests_retry_session().get(url)
        dataset_json = json.loads(response.text)
        for candle in reversed(dataset_json):
            kline = kline_object.kLine(candle)
            dataset.append(float(kline.CLOSE_PRICE))
        
        oldest_milisec = int(kline_object.kLine(dataset_json[0]).OPEN_TIME)
        latest_milisec = int(kline_object.kLine(dataset_json[int(count)-1]).OPEN_TIME)

    def getCurrentSMA(self, current_open_milis, current_close_price, window):
        global ma_cache
        global latest_milisec
        global window_last_added_latest_close_price
        no_of_adjustment = 0
        #check for need to update list of closing price
        if(current_open_milis != latest_milisec):
            self.adjustMADataset(current_close_price)

        #if in cache, use it, else do calculation
        if int(window) in ma_cache:
            old_summation = ma_cache[int(window)]

        else:
            old_summation = self.getMASum(window)

        new_summation = float(old_summation) - float(window_last_added_latest_close_price[int(window)]) + float(current_close_price)
        window_last_added_latest_close_price[int(window)] = float(current_close_price)
            
        ma_cache[int(window)] = new_summation
        return float(new_summation / int(window))


    def getMASum(self, window):
        global dataset
        global window_last_added_latest_close_price
        summation = 0
        for i in range(0, int(window)):
            summation += float(dataset[i])
        window_last_added_latest_close_price[int(window)] = float(dataset[0])
        return summation

    def adjustMADataset(self, new_close_price):
            #print(common.textWrapper('BLUE', 're-adjust ma by reloading'))
            #re-load dataset in
            global active_symbol
            global ma_cache
            global ds_count
            self.fetchdataset(active_symbol, ds_count)
            #recalculate cache
            for window, summation in ma_cache.items():
                ma_cache[int(window)] = self.getMASum(int(window))


        

