#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import numpy as np

from bwtougu.data.daybar_store import DayBarStore
from bwtougu.interface import AbstractDataSource
from bwtougu.utils.datetime_func import convert_date_to_int, convert_int_to_date
from bwtougu.data.converter import StockBarConverter, IndexBarConverter
from bwtougu.data.instrument_store import InstrumentStore
from bwtougu.data.dividend_store import DividendStore
from bwtougu.data.trading_dates_store import TradingDatesStore
from bwtougu.data.simple_factor_store import SimpleFactorStore
from bwtougu.data.date_set import DateSet
from bwtougu.utils.py2 import lru_cache
from bwtougu.data.yield_curve_store import YieldCurveStore

class BaseDataSource(AbstractDataSource):
    def __init__(self, path):
        if not os.path.exists(path):
            raise RuntimeError('bundle path {} not exist'.format(os.path.abspath))

        def _p(name):
            return os.path.join(path, name)

        self._day_bars = [
            DayBarStore(_p('stocks.bcolz'), StockBarConverter),
            DayBarStore(_p('indexes.bcolz'), IndexBarConverter),
        ]

        self._instruments = InstrumentStore(_p('instruments.pk'))
        self._dividends = DividendStore(_p('original_dividends.bcolz'))
        self._trading_dates = TradingDatesStore(_p('trading_dates.bcolz'))
        self._yield_curve = YieldCurveStore(_p('yield_curve.bcolz'))
        self._split_factor = SimpleFactorStore(_p('split_factor.bcolz'))
        self._ex_cum_factor = SimpleFactorStore(_p('ex_cum_factor.bcolz'))

        self._st_stock_days = DateSet(_p('st_stock_days.bcolz'))
        self._suspend_days = DateSet(_p('suspended_days.bcolz'))

        self.get_yield_curve = self._yield_curve.get_yield_curve
        self.get_risk_free_rate = self._yield_curve.get_risk_free_rate

    def get_trading_calendar(self):
        return self._trading_dates.get_trading_calendar()

    def get_all_instruments(self):
        return self._instruments.get_all_instruments()

    # 是否停牌
    def is_suspended(self, order_book_id, dates):
        return self._suspend_days.contains(order_book_id, dates)

    # 是否为st股票
    def is_st_stock(self, order_book_id, dates):
        return self._st_stock_days.contains(order_book_id, dates)

    INSTRUMENT_TYPE_MAP = {
        'CS': 0,
        'INDX': 1,
        'Future': 2,
        'ETF': 3,
        'LOF': 3,
        'FenjiA': 3,
        'FenjiB': 3,
        'FenjiMu': 3,
        'PublicFund': 4
    }

    def _index_of(self, instrument):
        return self.INSTRUMENT_TYPE_MAP[instrument.type]

    @lru_cache(None)
    def _all_day_bars_of(self, instrument):
        i = self._index_of(instrument)
        return self._day_bars[i].get_bars(instrument.order_book_id, fields=None)

    def get_bar(self, instrument, dt, frequency):
        if frequency != '1d':
            raise NotImplementedError

        bars = self._all_day_bars_of(instrument)
        if bars is None:
            return
        dt = np.uint64(convert_date_to_int(dt))
        pos = bars['datetime'].searchsorted(dt)
        if pos >= len(bars) or bars['datetime'][pos] != dt:
            return None

        return bars[pos]

    def available_data_range(self, frequency):
        if frequency in ['tick', '1d']:
            s, e = self._day_bars[self.INSTRUMENT_TYPE_MAP['INDX']].get_date_range('000001.XSHG')
            return convert_int_to_date(s).date(), convert_int_to_date(e).date()

        raise NotImplementedError

    def get_dividend(self, order_book_id, public_fund=False):
        if public_fund:
            return self._public_fund_dividends.get_dividend(order_book_id)
        return self._dividends.get_dividend(order_book_id)
