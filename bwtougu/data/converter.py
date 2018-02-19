#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import namedtuple

import numpy as np

Rule = namedtuple('Rule', ['dtype', 'multiplier', 'round'])

class Converter(object):
    def __init__(self, rules):
        self._rules = rules

    def convert(self, name, data):
        try:
            r = self._rules[name]
        except KeyError:
            return data

        result = data * r.multiplier
        if r.round:
            result = np.round(result, r.round)

        return result

    def field_type(self, name, dt):
        try:
            return self._rules[name].dtype
        except KeyError:
            return dt

float64 = np.dtype('float64')

StockBarConverter = Converter({
    'open': Rule(float64, 1 / 10000.0, 2),
    'close': Rule(float64, 1 / 10000.0, 2),
    'high': Rule(float64, 1 / 10000.0, 2),
    'low': Rule(float64, 1 / 10000.0, 2),
    'limit_up': Rule(float64, 1/10000.0, 2),
    'limit_down': Rule(float64, 1/10000.0, 2),
    'volume': Rule(float64, 1, 0),
})

IndexBarConverter = Converter({
    'open': Rule(float64, 1 / 10000.0, 2),
    'close': Rule(float64, 1 / 10000.0, 2),
    'high': Rule(float64, 1 / 10000.0, 2),
    'low': Rule(float64, 1 / 10000.0, 2),
    'volume': Rule(float64, 1, 0),
})

