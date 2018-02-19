#!/usr/bin/env python
# -*- coding: utf-8 -*-

import abc

from six import with_metaclass

from bwtougu.const import SIDE
from bwtougu.utils.exception import patch_user_exc
from bwtougu.utils.i18n import gettext as _


class BaseSlippage(with_metaclass(abc.ABCMeta)):
    @abc.abstractmethod
    def get_trade_price(self, order, price):
        raise NotImplementedError


class PriceRatioSlippage(BaseSlippage):
    def __init__(self, rate=0.):
        # Rate必须在0~1之间
        if 0 <= rate < 1:
            self.rate = rate
        else:
            raise patch_user_exc(ValueError(_(u"invalid slippage rate value: value range is [0, 1)")))

    def get_trade_price(self, side, price):
        return price + price * self.rate * (1 if side == SIDE.BUY else -1)


# class FixedSlippage(BaseSlippage):
#     def __init__(self, rate=0.):
#         self.rate = rate
#
#     def get_trade_price(self, price):
#         return price + price * self.rate * (0.5 if order.side == SIDE.BUY else -0.5)
