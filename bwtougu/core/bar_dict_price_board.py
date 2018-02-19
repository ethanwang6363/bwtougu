#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

from bwtougu.interface import AbstractPriceBoard
from bwtougu.environment import Environment


class BarDictPriceBoard(AbstractPriceBoard):
    def __init__(self):
        self._env = Environment.get_instance()

    @property
    def _bar_dict(self):
        return self._env.bar_dict

    def get_last_price(self, order_book_id):
        return np.nan if self._bar_dict.dt is None else self._bar_dict[order_book_id].last

    def get_limit_up(self, order_book_id):
        return np.nan if self._bar_dict.dt is None else self._bar_dict[order_book_id].limit_up

    def get_limit_down(self, order_book_id):
        return np.nan if self._bar_dict.dt is None else self._bar_dict[order_book_id].limit_down

    def get_a1(self, order_book_id):
        return np.nan

    def get_b1(self, order_book_id):
        return np.nan
