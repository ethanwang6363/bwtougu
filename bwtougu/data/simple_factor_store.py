#!/usr/bin/env python
# -*- coding: utf-8 -*-

import bcolz


class SimpleFactorStore(object):
    def __init__(self, f):
        table = bcolz.open(f, 'r')
        self._index = table.attrs['line_map']
        self._table = table[:]

    def get_factors(self, order_book_id):
        try:
            s, e = self._index[order_book_id]
            return self._table[s:e]
        except KeyError:
            return None
