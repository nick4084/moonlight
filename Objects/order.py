#!/usr/bin/python

import trade

class Order:

    PARAM_STATUS_NEW = 'NEW'
    PARAM_STATUS_PARTIALLY_FILLED = 'PARTIALLY_FILLED'
    PARAM_STATUS_FILLED = 'FILLED'
    PARAM_STATUS_CANCELED = 'CANCELED'
    #PARAM_STATUS_PENDING_CANCEL = 'PENDING_CANCEL' (currently unused)
    PARAM_STATUS_REJECTED = 'REJECTED'
    PARAM_STATUS_EXPIRED = 'EXPIRED'

    def __init__(self, order_arr):
        self.order = order_arr

        self.SYMBOL = self.order['symbol']
        self.ORDER_ID = self.order['orderId']
        self.CLIENT_ORDER_ID = self.order['clientOrderId']
        self.PRICE = self.order['price']
        self.ORIG_QTY = self.order['origQty'] 
        self.EXECUTED_QTY = self.order['executedQty']
        self.CUMMULATIVE_QUOTE_QTY = self.order['cummulativeQuoteQty']
        self.STATUS = self.order['status'] 
        self.TIME_IN_FORCE = self.order['timeInForce'] 
        self.TYPE = self.order['type']
        self.SIDE = self.order['side'] 
        self.STOP_PRICE = self.order['stopPrice'] 
        self.ICEBERG_QTY = self.order['icebergQty'] 
        self.TIME = self.order['time']
        self.UPDATE_TIME = self.order['updateTime']
        self.IS_WORKING = self.order['isWorking']

    def cancelOrder(self):
        print(str(self.ORDER_ID))
        trade.cancelOrder(
        self.SYMBOL,
        self.ORDER_ID
        )

    def is_filled(self):
        if(self.STATUS == self.PARAM_STATUS_FILLED):
            return True
        else:
            return False

    def is_canceled(self):
        if(self.STATUS == self.PARAM_STATUS_CANCELED):
            return True
        else:
            return False

    def is_new(self):
        if(self.STATUS == self.PARAM_STATUS_NEW):
            return True
        else:
            return False

    def is_partially_filled(self):
        if(self.STATUS == self.PARAM_STATUS_PARTIALLY_FILLED):
            return True
        else:
            return False


    def has_limit_order(self):
        if(self.STATUS == self.PARAM_STATUS_NEW or self.STATUS == self.PARAM_STATUS_PARTIALLY_FILLED):
            return True
        else:
            return False

