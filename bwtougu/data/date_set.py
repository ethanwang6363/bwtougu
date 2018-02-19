#!/usr/bin/env python
# -*- coding: utf-8 -*-


import bcolz
import numpy as np

from bwtougu.utils.py2 import lru_cache


class DateSet(object):
    def __init__(self, f):
        dates = bcolz.open(f, 'r')
        self._index = dates.attrs['line_map']
        self._dates = dates[:]

    @lru_cache(None)
    def _get_set(self, s, e):
        return set(self._dates[s:e].tolist())

    def get_days(self, order_book_id):
        try:
            s, e = self._index[order_book_id]
        except KeyError:
            return []

        return self._get_set(s, e)

    def contains(self, order_book_id, dates):
        try:
            s, e = self._index[order_book_id]
        except KeyError:
            return [False] * len(dates)

        def _to_dt_int(d):
            if isinstance(d, (int, np.int64, np.uint64)):
                return int(d // 1000000) if d > 100000000 else int(d)
            else:
                return d.year*10000 + d.month*100 + d.day

        date_set = self._get_set(s, e)

        return [(_to_dt_int(d) in date_set) for d in dates]
