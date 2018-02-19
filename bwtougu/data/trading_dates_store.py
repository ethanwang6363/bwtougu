#!/usr/bin/env python
# -*- coding: utf-8 -*-


import bcolz
import pandas as pd


class TradingDatesStore(object):
    def __init__(self, f):
        self._dates = pd.Index(pd.Timestamp(str(d)) for d in bcolz.open(f, 'r'))

    def get_trading_calendar(self):
        return self._dates

