#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logbook
import six
import pytz
import datetime

from bwtougu import const
from bwtougu.environment import Environment
from bwtougu.core.global_var import GlobalVars
from bwtougu.core.strategy_universe import StrategyUniverse
from bwtougu.mod import ModHandler

from bwtougu.model.portfolio import Portfolio
from bwtougu.model.base_position import Positions
from bwtougu.model.bar import BarMap

from bwtougu.core.strategy_loader import FileStrategyLoader
from bwtougu.data.base_data_source import BaseDataSource
from bwtougu.data.data_proxy import DataProxy
from bwtougu.utils.i18n import gettext as _
from bwtougu.utils.scheduler import Scheduler
from bwtougu.utils.exception import CustomException, patch_user_exc
from bwtougu.utils import create_custom_exception, run_with_user_log_disabled, scheduler as mod_scheduler
from bwtougu.execution_context import ExecutionContext
from bwtougu.events import EVENT, Event
from bwtougu.core.strategy_context import StrategyContext
from bwtougu.core.strategy import Strategy
from bwtougu.utils.logger import system_log

from bwtougu.api import helper as api_helper

def run(config, source_code=None, user_funcs=None):
    env = Environment(config)
    persist_helper = None
    init_succeed = False
    mod_handler = ModHandler()

    try:
        set_loggers(config)
        env.set_strategy_loader(FileStrategyLoader(config.base.strategy_file))
        env.set_global_vars(GlobalVars())
        mod_handler.set_env(env)
        mod_handler.start_up()

        if not env.data_source:
            env.set_data_source(BaseDataSource(config.base.data_bundle_path))
        env.set_data_proxy(DataProxy(env.data_source))

        Scheduler.set_trading_dates_(env.data_source.get_trading_calendar())
        scheduler = Scheduler(config.base.frequency)
        mod_scheduler._scheduler = scheduler

        env._universe = StrategyUniverse()
        _adjust_start_date(env.config, env.data_proxy)
        _validate_benchmark(env.config, env.data_proxy)

        start_dt = datetime.datetime.combine(config.base.start_date, datetime.datetime.min.time())
        env.calendar_dt = start_dt
        env.trading_dt = start_dt

        broker = env.broker
        assert broker is not None
        env.portfolio = broker.get_portfolio()
        env.benchmark_portfolio = create_benchmark_portfolio(env)

        event_source = env.event_source
        assert event_source is not None

        bar_dict = BarMap(env.data_proxy, config.base.frequency)
        env.set_bar_dict(bar_dict)

        if env.price_board is None:
            from .core.bar_dict_price_board import BarDictPriceBoard
            env.price_board = BarDictPriceBoard()

        ctx = ExecutionContext(const.EXECUTION_PHASE.GLOBAL)
        ctx._push()

        env.event_bus.publish_event(Event(EVENT.POST_SYSTEM_INIT))

        scope = create_base_scope()
        scope.update({
            "g": env.global_vars
        })

        apis = api_helper.get_apis()
        scope.update(apis)

        scope = env.strategy_loader.load(scope)

        ucontext = StrategyContext()
        user_strategy = Strategy(env.event_bus, scope, ucontext)
        scheduler.set_user_context(ucontext)

        if not config.extra.force_run_init_when_pt_resume:
            with run_with_user_log_disabled(disabled=config.base.resume_mode):
                user_strategy.init()

        init_succeed = True

        from .core.executor import Executor
        Executor(env).run(bar_dict)

        result = mod_handler.tear_down(const.EXIT_CODE.EXIT_SUCCESS)
        system_log.debug(_(u"strategy run successfully, normal exit"))
        return result
    except Exception as e:
        six.print_(e)
        raise e


def _adjust_start_date(config, data_proxy):
    origin_start_date, origin_end_date = config.base.start_date, config.base.end_date
    start, end = data_proxy.available_data_range(config.base.frequency)

    config.base.start_date = max(start, config.base.start_date)
    config.base.end_date = min(end, config.base.end_date)
    config.base.trading_calendar = data_proxy.get_trading_dates(config.base.start_date, config.base.end_date)
    if len(config.base.trading_calendar) == 0:
        raise patch_user_exc(ValueError(_(u"There is no data between {start_date} and {end_date}. Please check your"
                                          u" data bundle or select other backtest period.").format(
            start_date=origin_start_date, end_date=origin_end_date)))
    config.base.start_date = config.base.trading_calendar[0].date()
    config.base.end_date = config.base.trading_calendar[-1].date()
    config.base.timezone = pytz.utc

def set_loggers(config):
    from bwtougu.utils.logger import user_log, system_log
    from bwtougu.utils.logger import user_std_handler, init_logger
    from bwtougu.utils import logger
    extra_config = config.extra

    init_logger()

    for log in [system_log, user_log]:
        log.level = getattr(logbook, config.extra.log_level.upper(), logbook.NOTSET)

    if extra_config.log_level.upper() != "NONE":
        if not extra_config.user_log_disabled:
            user_log.handlers.append(user_std_handler)

    for logger_name, level in extra_config.logger:
        getattr(logger, logger_name).level = getattr(logbook, level.upper())


def _validate_benchmark(config, data_proxy):
    benchmark = config.base.benchmark
    if benchmark is None:
        return
    instrument = data_proxy.instruments(benchmark)
    if instrument is None:
        raise patch_user_exc(ValueError(_(u"invalid benchmark {}").format(benchmark)))

    if instrument.order_book_id == "000300.XSHG":
        # 000300.XSHG 数据进行了补齐，因此认为只要benchmark设置了000300.XSHG，就存在数据，不受限于上市日期。
        return
    config = Environment.get_instance().config
    start_date = config.base.start_date
    end_date = config.base.end_date
    if instrument.listed_date.date() > start_date:
        raise patch_user_exc(ValueError(
            _(u"benchmark {benchmark} has not been listed on {start_date}").format(benchmark=benchmark,
                                                                                   start_date=start_date)))
    if instrument.de_listed_date.date() < end_date:
        raise patch_user_exc(ValueError(
            _(u"benchmark {benchmark} has been de_listed on {end_date}").format(benchmark=benchmark,
                                                                                end_date=end_date)))

def create_benchmark_portfolio(env):
    if env.config.base.benchmark is None:
        return None

    BenchmarkAccount = env.get_account_model(const.DEFAULT_ACCOUNT_TYPE.BENCHMARK.name)
    BenchmarkPosition = env.get_position_model(const.DEFAULT_ACCOUNT_TYPE.BENCHMARK.name)

    start_date = env.config.base.start_date
    total_cash = sum(env.config.base.accounts.values())
    accounts = {
        const.DEFAULT_ACCOUNT_TYPE.BENCHMARK.name: BenchmarkAccount(total_cash, Positions(BenchmarkPosition))
    }
    return Portfolio(start_date, 1, total_cash, accounts)

def create_base_scope():
    import copy
    from bwtougu.utils.logger import user_print, user_log

    from . import user_module
    scope = copy.copy(user_module.__dict__)
    scope.update({
        "logger": user_log,
        "print": user_print,
    })

    return scope

