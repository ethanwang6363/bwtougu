#!/usr/bin/env python
# -*- coding: utf-8 -*-


import bcolz
import pandas as pd
import numpy as np

# from bwtougu.data import risk_free_helper


class YieldCurveStore(object):
    def __init__(self, f):
        self._table = bcolz.open(f, 'r')
        self._dates = self._table.cols['date'][:]

    def get_yield_curve(self, start_date, end_date, tenor):
        d1 = start_date.year * 10000 + start_date.month * 100 + start_date.day
        d2 = end_date.year * 10000 + end_date.month * 100 + end_date.day

        s = self._dates.searchsorted(d1)
        e = self._dates.searchsorted(d2, side='right')

        if e == len(self._dates):
            e -= 1
        if self._dates[e] == d2:
            # 包含 end_date
            e += 1

        if e < s:
            return None

        df = pd.DataFrame(self._table[s:e])
        df.index = pd.Index(pd.Timestamp(str(d)) for d in df['date'])
        del df['date']

        df.rename(columns=lambda n: n[1:]+n[0], inplace=True)
        if tenor is not None:
            return df[tenor]
        return df

    def get_risk_free_rate(self, start_date, end_date):
        raise NotImplementedError
        '''
        tenor = risk_free_helper.get_tenor_for(start_date, end_date)
        tenor = tenor[-1] + tenor[:-1]
        d = start_date.year * 10000 + start_date.month * 100 + start_date.day
        pos = self._dates.searchsorted(d)
        if pos > 0 and (pos == len(self._dates) or self._dates[pos] != d):
            pos -= 1

        col = self._table.cols[tenor]
        while pos >= 0 and np.isnan(col[pos]):
            # data is missing ...
            pos -= 1

        return self._table.cols[tenor][pos]
        '''
