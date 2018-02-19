#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import abc
from six import with_metaclass

class AbstractMod(with_metaclass(abc.ABCMeta)):
    """
    扩展模块接口
    """
    @abc.abstractmethod
    def start_up(self, env, mod_config):
        raise NotImplementedError

    def tear_down(self, code, exception=None):
        raise NotImplementedError


class AbstractStrategyLoader(with_metaclass(abc.ABCMeta)):
    @abc.abstractmethod
    def load(self, scope):
        raise NotImplementedError

class AbstractEventSource(with_metaclass(abc.ABCMeta)):
    @abc.abstractmethod
    def events(self, start_date, end_date, frequency):
        raise NotImplementedError

class AbstractDataSource(object):
    def get_all_instruments(self):
        raise NotImplementedError

    def get_trading_calendar(self):
        raise NotImplementedError

    def get_dividend(self, order_book_id):
        raise NotImplementedError

    def get_split(self, order_book_id):
        raise NotImplementedError

    def get_bar(self, instrument, dt, frequency):
        raise NotImplementedError

    def history_bars(self, instrument, bar_count, frequency, fields, dt, skip_suspended=True,
                     include_now=False, adjust_type='pre', adjust_orig=None):
        raise NotImplementedError

    def current_snapshot(self, instrument, frequency, dt):
        raise NotImplementedError

    def available_data_range(self, frequency):
        raise NotImplementedError


class AbstractBroker(with_metaclass(abc.ABCMeta)):
    """
    券商接口。

    RQAlpha 将产生的订单提交给此对象，此对象负责对订单进行撮合（不论是自行撮合还是委托给外部的真实交易所），
    并通过 ``EVENT.ORDER_*`` 及 ``EVENT.TRADE`` 事件将撮合结果反馈进入 RQAlpha。

    在扩展模块中，可以通过调用 ``env.set_broker`` 来替换默认的 Broker。
    """

    @abc.abstractmethod
    def get_portfolio(self):
        """
        [Required]

        获取投资组合。系统初始化时，会调用此接口，获取包含账户信息、净值、份额等内容的投资组合

        :return: Portfolio
        """

    @abc.abstractmethod
    def submit_order(self, order):
        """
        [Required]

        提交订单。在当前版本，RQAlpha 会生成 :class:`~Order` 对象，再通过此接口提交到 Broker。
        TBD: 由 Broker 对象生成 Order 并返回？
        """
        raise NotImplementedError

    @abc.abstractmethod
    def cancel_order(self, order):
        """
        [Required]

        撤单。

        :param order: 订单
        :type order: :class:`~Order`
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_open_orders(self, order_book_id=None):
        """
        [Required]

        获得当前未完成的订单。

        :return: list[:class:`~Order`]
        """
        raise NotImplementedError

class AbstractPosition(with_metaclass(abc.ABCMeta)):
    """
    仓位接口，主要用于构建仓位信息

    您可以在 Mod 的 start_up 阶段通过 env.set_position_model(account_type, PositionModel) 来注入和修改 PositionModel
    您也可以通过 env.get_position_model(account_type) 来获取制定类型的 PositionModel
    """

    @abc.abstractmethod
    def get_state(self):
        """
        [Required]

        主要用于进行持久化时候，提供对应需要持久化的数据
        """
        raise NotImplementedError

    @abc.abstractmethod
    def set_state(self, state):
        """
        [Requried]

        主要用于持久化恢复时，根据提供的持久化数据进行恢复 Position 的实现
        """
        raise NotImplementedError

    @abc.abstractmethod
    def order_book_id(self):
        """
        [Required]

        返回当前持仓的 order_book_id
        """
        raise NotImplementedError

    @abc.abstractproperty
    def type(self):
        """
        [Required]

        返回 String 类型的账户类型标示
        """
        raise NotImplementedError

    @abc.abstractproperty
    def market_value(self):
        """
        [Required]

        返回当前持仓的市值
        """
        raise NotImplementedError

    @abc.abstractproperty
    def transaction_cost(self):
        """
        [Required]

        返回当前持仓的当日交易费用
        """
        raise NotImplementedError

class AbstractPriceBoard(with_metaclass(abc.ABCMeta)):
    """
    RQAlpha多个地方需要使用最新「行情」，不同的数据源其最新价格获取的方式不尽相同

    因此抽离出 `AbstractPriceBoard`, 您可以自行进行扩展并替换默认 PriceBoard
    """
    @abc.abstractmethod
    def get_last_price(self, order_book_id):
        """
        获取证券的最新价格
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_limit_up(self, order_book_id):
        raise NotImplementedError

    @abc.abstractmethod
    def get_limit_down(self, order_book_id):
        raise NotImplementedError

    def get_a1(self, order_book_id):
        raise NotImplementedError

    def get_b1(self, order_book_id):
        raise NotImplementedError


class AbstractAccount(with_metaclass(abc.ABCMeta)):
    """
    账户接口，主要用于构建账户信息

    您可以在 Mod 的 start_up 阶段通过 env.set_account_model(account_type, AccountModel) 来注入和修改 AccountModel
    您也可以通过 env.get_account_model(account_type) 来获取指定类型的 AccountModel
    """
    @abc.abstractmethod
    def fast_forward(self, orders, trades):
        """
        [Required]

        fast_forward 函数接受当日订单数据和成交数据，从而将当前的持仓快照快速推进到最新持仓状态

        :param list orders: 当日订单列表
        :param list trades: 当日成交列表
        """
        raise NotImplementedError

    @abc.abstractmethod
    def order(self, order_book_id, quantity, style, target=False):
        """
        [Required]

        系统下单函数会调用该函数来完成下单操作
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_state(self):
        """
        [Required]

        主要用于进行持久化时候，提供对应需要持久化的数据
        """
        raise NotImplementedError

    @abc.abstractmethod
    def set_state(self, state):
        """
        [Requried]

        主要用于持久化恢复时，根据提供的持久化数据进行恢复Account的实现
        """
        raise NotImplementedError

    @abc.abstractproperty
    def type(self):
        """
        [Required]

        返回 String 类型的账户类型标示
        """
        raise NotImplementedError

    @abc.abstractproperty
    def positions(self):
        """
        [Required]

        返回当前账户的持仓数据

        :return: Positions(PositionModel)
        """
        raise NotImplementedError

    @abc.abstractproperty
    def frozen_cash(self):
        """
        [Required]

        返回当前账户的冻结资金
        """
        raise NotImplementedError

    @abc.abstractproperty
    def cash(self):
        """
        [Required]

        返回当前账户的可用资金
        """
        raise NotImplementedError

    @abc.abstractproperty
    def market_value(self):
        """
        [Required]

        返回当前账户的市值
        """
        raise NotImplementedError

    @abc.abstractproperty
    def transaction_cost(self):
        """
        [Required]

        返回当前账户的当日交易费用
        """
        raise NotImplementedError


class Persistable(with_metaclass(abc.ABCMeta)):
    @abc.abstractmethod
    def get_state(self):
        """
        :return: bytes
        """
        raise NotImplementedError

    @abc.abstractmethod
    def set_state(self, state):
        """
        :param state: bytes
        :return:
        """
        raise NotImplementedError

    @classmethod
    def __subclasshook__(cls, C):
        if cls is Persistable:
            if (any("get_state" in B.__dict__ for B in C.__mro__) and
                    any("set_state" in B.__dict__ for B in C.__mro__)):
                return True
        return NotImplemented