#!/usr/bin/python
import settings as s
import json
from binance.client import Client
from binance.enums import *

#limit
def buy_limit(sym, qty, price):
    order = s.client.order_limit_buy(
    symbol=sym,
    quantity=qty,
    price=price)

    return order

def sell_limit(sym, qty, price):
    order = s.client.order_limit_sell(
    symbol=sym,
    quantity=qty,
    price=price)

    return order

#market
def buy_market(sym, qty):
    order = s.client.order_market_buy(
    symbol=sym,
    quantity=qty)

    return order

def sell_market(sym, qty):
    order = s.client.order_market_sell(
    symbol=sym,
    quantity=qty)

    return order

#get orders in place
def getAllOrder(sym):
    return s.client.get_all_orders(symbol=sym)

def getLastOrder(sym):
    return s.client.get_all_orders(symbol=sym, limit=1)

def getOrderStatus(sym, order_id):
    order = s.client.get_order(
    symbol=sym,
    orderId=order_id)

    return order

def cancelOrder(sym, order_id):
    result = s.client.cancel_order(
    symbol=sym,
    orderId=order_id)

    return result

def getMyTrades(sym):
    result = s.client.get_my_trades(
    symbol = sym
    )
    return result

#depth
def getOrderBook(sym):
    result = s.client.get_order_book(
    symbol=str(sym))

    return result







