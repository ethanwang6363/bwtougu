#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pprint
import re
import six
import collections
import numpy as np

from bwtougu.utils.exception import CustomError, CustomException
from bwtougu.const import INSTRUMENT_TYPE, DEFAULT_ACCOUNT_TYPE
from bwtougu.const import EXC_TYPE
from contextlib import contextmanager
from bwtougu.utils.i18n import gettext as _

from bwtougu.utils.py2 import lru_cache



class RqAttrDict(object):

    def __init__(self, d=None):
        self.__dict__ = d if d is not None else dict()

        for k, v in list(six.iteritems(self.__dict__)):
            if isinstance(v, dict):
                self.__dict__[k] = RqAttrDict(v)

    def __repr__(self):
        return pprint.pformat(self.__dict__)

    def __iter__(self):
        return self.__dict__.__iter__()

    def update(self, other):
        RqAttrDict._update_dict_recursive(self, other)

    def items(self):
        return six.iteritems(self.__dict__)

    iteritems = items

    def keys(self):
        return self.__dict__.keys()

    @staticmethod
    def _update_dict_recursive(target, other):
        if isinstance(other, RqAttrDict):
            other = other.__dict__
        if isinstance(target, RqAttrDict):
            target = target.__dict__

        for k, v in six.iteritems(other):
            if isinstance(v, collections.Mapping):
                r = RqAttrDict._update_dict_recursive(target.get(k, {}), v)
                target[k] = r
            else:
                target[k] = other[k]
        return target

    def convert_to_dict(self):
        result_dict = {}
        for k, v in list(six.iteritems(self.__dict__)):
            if isinstance(v, RqAttrDict):
                v = v.convert_to_dict()
            result_dict[k] = v
        return result_dict


def generate_account_type_dict():
    account_type_dict = {}
    for key, a_type in six.iteritems(DEFAULT_ACCOUNT_TYPE.__members__):
        account_type_dict[key] = a_type.value
    return account_type_dict


def instrument_type_str2enum(type_str):
    if type_str == "CS":
        return INSTRUMENT_TYPE.CS
    elif type_str == "Future":
        return INSTRUMENT_TYPE.FUTURE
    elif type_str == "Option":
        return INSTRUMENT_TYPE.OPTION
    elif type_str == "ETF":
        return INSTRUMENT_TYPE.ETF
    elif type_str == "LOF":
        return INSTRUMENT_TYPE.LOF
    elif type_str == "INDX":
        return INSTRUMENT_TYPE.INDX
    elif type_str == "FenjiMu":
        return INSTRUMENT_TYPE.FENJI_MU
    elif type_str == "FenjiA":
        return INSTRUMENT_TYPE.FENJI_A
    elif type_str == "FenjiB":
        return INSTRUMENT_TYPE.FENJI_B
    elif type_str == 'PublicFund':
        return INSTRUMENT_TYPE.PUBLIC_FUND
    else:
        raise NotImplementedError


def create_custom_exception(exc_type, exc_val, exc_tb, strategy_filename):
    try:
        msg = str(exc_val)
    except:
        msg = ""

    error = CustomError()
    error.set_msg(msg)
    error.set_exc(exc_type, exc_val, exc_tb)

    import linecache

    filename = ''
    tb = exc_tb
    while tb:
        co = tb.tb_frame.f_code
        filename = co.co_filename
        if filename != strategy_filename:
            tb = tb.tb_next
            continue
        lineno = tb.tb_lineno
        func_name = co.co_name
        code = linecache.getline(filename, lineno).strip()
        error.add_stack_info(filename, lineno, func_name, code, tb.tb_frame.f_locals)
        tb = tb.tb_next

    if filename == strategy_filename:
        error.error_type = EXC_TYPE.USER_EXC

    user_exc = CustomException(error)
    return user_exc


@contextmanager
def run_with_user_log_disabled(disabled=True):
    from rqalpha.utils.logger import user_log

    if disabled:
        user_log.disable()
    try:
        yield
    finally:
        if disabled:
            user_log.enable()

@lru_cache(None)
def get_account_type(order_book_id):
    from bwtougu.environment import Environment
    instrument = Environment.get_instance().get_instrument(order_book_id)
    enum_type = instrument.enum_type
    if enum_type in INST_TYPE_IN_STOCK_ACCOUNT:
        return DEFAULT_ACCOUNT_TYPE.STOCK.name
    elif enum_type == INSTRUMENT_TYPE.FUTURE:
        return DEFAULT_ACCOUNT_TYPE.FUTURE.name
    else:
        raise NotImplementedError

INST_TYPE_IN_STOCK_ACCOUNT = [
    INSTRUMENT_TYPE.CS,
    INSTRUMENT_TYPE.ETF,
    INSTRUMENT_TYPE.LOF,
    INSTRUMENT_TYPE.INDX,
    INSTRUMENT_TYPE.FENJI_MU,
    INSTRUMENT_TYPE.FENJI_A,
    INSTRUMENT_TYPE.FENJI_B,
    INSTRUMENT_TYPE.PUBLIC_FUND
]


def merge_dicts(*dict_args):
    result = {}
    for d in dict_args:
        result.update(d)
    return result

def to_industry_code(s):
    from bwtougu.model.instrument import IndustryCode, IndustryCodeItem

    for __, v in six.iteritems(IndustryCode.__dict__):
        if isinstance(v, IndustryCodeItem):
            if v.name == s:
                return v.code
    return s

def to_sector_name(s):
    from bwtougu.model.instrument import SectorCode, SectorCodeItem

    for __, v in six.iteritems(SectorCode.__dict__):
        if isinstance(v, SectorCodeItem):
            if v.cn == s or v.en == s or v.name == s:
                return v.name
    # not found
    return s

def unwrapper(func):
    f2 = func
    while True:
        f = f2
        f2 = getattr(f2, "__wrapped__", None)
        if f2 is None:
            break
    return f

def run_when_strategy_not_hold(func):
    from bwtougu.environment import Environment
    from bwtougu.utils.logger import system_log

    def wrapper(*args, **kwargs):
        if not Environment.get_instance().config.extra.is_hold:
            return func(*args, **kwargs)
        else:
            system_log.debug(_(u"not run {}({}, {}) because strategy is hold").format(func, args, kwargs))

    return wrapper


def id_gen(start=1):
    i = start
    while True:
        yield i
        i += 1

def is_valid_price(price):
    return not np.isnan(price) and price > 0

