#!/usr/bin env python
# -*- coding: utf-8 -*-

from bwtougu.data.instrument_mixin import InstrumentMixin
from bwtougu.data.trading_dates_mixin import TradingDatesMixin

class DataProxy(InstrumentMixin, TradingDatesMixin):
    def __init__(self, data_source):
        self._data_source = data_source
        try:
            self.get_risk_free_rate = data_source.get_risk_free_rate
        except AttributeError:
            pass
        InstrumentMixin.__init__(self, data_source.get_all_instruments())
        TradingDatesMixin.__init__(self, data_source.get_trading_calendar())

    def __getattr__(self, item):
        return getattr(self._data_source, item)
