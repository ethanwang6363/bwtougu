#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bwtougu.const import DEFAULT_ACCOUNT_TYPE

from .commission import StockCommission, FutureCommission
from .slippage import PriceRatioSlippage
from .tax import StockTax, FutureTax


class CommissionDecider(object):
    def __init__(self, multiplier):
        self.deciders = dict()
        self.deciders[DEFAULT_ACCOUNT_TYPE.STOCK.name] = StockCommission(multiplier)
        self.deciders[DEFAULT_ACCOUNT_TYPE.FUTURE.name] = FutureCommission(multiplier)

    def get_commission(self, account_type, trade):
        return self.deciders[account_type].get_commission(trade)


class SlippageDecider(object):
    def __init__(self, rate):
        self.decider = PriceRatioSlippage(rate)

    def get_trade_price(self, side, price):
        return self.decider.get_trade_price(side, price)


class TaxDecider(object):
    def __init__(self, rate=None):
        self.deciders = dict()
        self.deciders[DEFAULT_ACCOUNT_TYPE.STOCK.name] = StockTax(rate)
        self.deciders[DEFAULT_ACCOUNT_TYPE.BENCHMARK.name] = StockTax(rate)
        self.deciders[DEFAULT_ACCOUNT_TYPE.FUTURE.name] = FutureTax(rate)

    def get_tax(self, account_type, trade):
        return self.deciders[account_type].get_tax(trade)
