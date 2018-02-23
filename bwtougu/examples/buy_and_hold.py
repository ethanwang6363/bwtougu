#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bwtougu.api import *

def init(context):
    logger.info("init00")
    context.s1 = "000001.XSHE"
    context.fired = False

def before_trading(context):
    pass

def handle_bar(context, bar_dict):
    logger.info(context.s1 + ", frequency:" + bar_dict._frequency + ", date: " + str(bar_dict.dt))

    if not context.fired:
        # order_percent并且传入1代表买入该股票并且使其占有投资组合的100%
        order_percent(context.s1, 1)
        context.fired = True
