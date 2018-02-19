#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bwtougu.environment import Environment
from bwtougu.events import EVENT
from bwtougu.utils import is_valid_price

from .stock_account import StockAccount


class BenchmarkAccount(StockAccount):
    def __init__(self, total_cash, positions, backward_trade_set=set(), dividend_receivable=None):
        super(BenchmarkAccount, self).__init__(total_cash, positions, backward_trade_set, dividend_receivable)
        self.benchmark = Environment.get_instance().config.base.benchmark

    def register_event(self):
        event_bus = Environment.get_instance().event_bus
        event_bus.prepend_listener(EVENT.SETTLEMENT, self._on_settlement)
        event_bus.prepend_listener(EVENT.PRE_BEFORE_TRADING, self._before_trading)
        event_bus.prepend_listener(EVENT.PRE_BAR, self._on_bar)
        event_bus.prepend_listener(EVENT.TICK, self._on_tick)

    def _on_bar(self, event):
        # run once
        if len(self._positions) == 0:
            price = event.bar_dict[self.benchmark].close
            if not is_valid_price(price):
                return
            position = self._positions.get_or_create(self.benchmark)
            quantity = int(self._total_cash / price)
            position._quantity = quantity
            position._avg_price = price
            self._total_cash -= quantity * price

    def _on_tick(self, event):
        # run once
        if len(self._positions) == 0:
            tick = event.tick
            if tick.order_book_id != self.benchmark:
                return
            price = tick.last
            position = self._positions.get_or_create(self.benchmark)
            quantity = int(self._total_cash / price)
            position._quantity = quantity
            position._avg_price = price
            self._total_cash -= quantity * price
