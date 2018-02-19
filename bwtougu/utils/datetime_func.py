#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from bwtougu.utils.py2 import lru_cache

def convert_date_to_int(dt):
    t = dt.year * 10000 + dt.month * 100 + dt.day
    t *= 1000000
    return t

def convert_int_to_date(dt_int):
    dt_int = int(dt_int)
    if dt_int > 100000000:
        dt_int //= 1000000
    return _convert_int_to_date(dt_int)

@lru_cache(None)
def _convert_int_to_date(dt_int):
    year, r = divmod(dt_int, 10000)
    month, day = divmod(r, 100)
    return datetime.datetime(year, month, day)

@lru_cache(20480)
def convert_int_to_datetime(dt_int):
    dt_int = int(dt_int)
    year, r = divmod(dt_int, 10000000000)
    month, r = divmod(r, 100000000)
    day, r = divmod(r, 1000000)
    hour, r = divmod(r, 10000)
    minute, second = divmod(r, 100)
    return datetime.datetime(year, month, day, hour, minute, second)