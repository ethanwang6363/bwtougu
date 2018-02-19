#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum
from collections import defaultdict

class Event(object):
    def __init__(self, event_type, **kwargs):
        self.__dict__ = kwargs
        self.event_type = event_type

    def __repr__(self):
        return ' '.join('{}:{}'.format(k, v) for k, v in self.__dict__.items())


class EventBus(object):
    def __init__(self):
        self._listeners = defaultdict(list)

    def add_listener(self, event, listener):
        self._listeners[event].append(listener)

    def prepend_listener(self, event, listener):
        self._listeners[event].insert(0, listener)

    def publish_event(self, event):
        for l in self._listeners[event.event_type]:
            if l(event):
                break


class EVENT(Enum):

    POST_SYSTEM_INIT = 'post_system_init'

    POST_SYSTEM_RESTORED = 'post_system_restored'

    POST_USER_INIT = 'post_user_init'

    POST_UNIVERSE_CHANGED = 'post_universe_changed'

    PRE_BEFORE_TRADING = 'pre_before_trading'

    BEFORE_TRADING = 'before_trading'

    POST_BEFORE_TRADING = 'post_before_trading'

    PRE_BAR = 'pre_bar'

    BAR = 'bar'

    POST_BAR = 'post_bar'

    PRE_TICK = 'pre_tick'

    TICK = 'tick'

    POST_TICK = 'post_tick'

    PRE_SCHEDULED = 'pre_scheduled'

    POST_SCHEDULED = 'post_scheduled'

    PRE_AFTER_TRADING = 'pre_after_trading'

    AFTER_TRADING = 'after_trading'

    POST_AFTER_TRADING = 'post_after_trading'

    PRE_SETTLEMENT = 'pre_settlement'

    SETTLEMENT = 'settlement'

    POST_SETTLEMENT = 'post_settlement'

    ORDER_PENDING_NEW = 'order_pending_new'

    ORDER_CREATION_PASS = 'order_creation_pass'

    ORDER_CREATION_REJECT = 'order_creation_reject'

    ORDER_PENDING_CANCEL = 'order_pending_cancel'

    ORDER_CANCELLATION_PASS = 'order_cancellation_pass'

    ORDER_CANCELLATION_REJECT = 'order_cancellation_reject'

    ORDER_UNSOLICITED_UPDATE = 'order_unsolicited_update'

    TRADE = 'trade'

    ON_LINE_PROFILER_RESULT = 'on_line_profiler_result'

    DO_PERSIST = 'do_persist'

    STRATEGY_HOLD_SET = 'strategy_hold_set'

    STRATEGY_HOLD_CANCELLED = 'stragety_hold_canceled'


def parse_event(event_str):
    return EVENT.__members__.get(event_str.upper(), None)




