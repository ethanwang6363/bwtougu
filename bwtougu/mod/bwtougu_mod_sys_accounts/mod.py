#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bwtougu.interface import AbstractMod
from bwtougu.const import DEFAULT_ACCOUNT_TYPE
from bwtougu import export_as_api

from .account_model import StockAccount, BenchmarkAccount
from .position_model import StockPosition
from .api import api_stock

class AccountMod(AbstractMod):

    def start_up(self, env, mod_config):

        StockPosition.stock_t1 = mod_config.stock_t1

        # 注入 Account
        env.set_account_model(DEFAULT_ACCOUNT_TYPE.STOCK.name, StockAccount)
        # env.set_account_model(DEFAULT_ACCOUNT_TYPE.FUTURE.name, FutureAccount)
        env.set_account_model(DEFAULT_ACCOUNT_TYPE.BENCHMARK.name, BenchmarkAccount)

        # 注入 Position
        env.set_position_model(DEFAULT_ACCOUNT_TYPE.STOCK.name, StockPosition)
        # env.set_position_model(DEFAULT_ACCOUNT_TYPE.FUTURE.name, FuturePosition)
        env.set_position_model(DEFAULT_ACCOUNT_TYPE.BENCHMARK.name, StockPosition)

        # 注入 API
        if DEFAULT_ACCOUNT_TYPE.STOCK.name in env.config.base.accounts:
            # 注入股票API
            for export_name in api_stock.__all__:
                export_as_api(getattr(api_stock, export_name))

    def tear_down(self, code, exception=None):
        pass
