#!/usr/bin/env python
# -*- coding: utf-8 -*-

import bcolz
import numpy as np
import six

from bwtougu.utils.i18n import gettext as _

class DayBarStore(object):
    def __init__(self, main, converter):
        self._table = bcolz.open(main, 'r')
        self._index = self._table.attrs['line_map']
        self._converter = converter

    @staticmethod
    def _remove_(l, v):
        try:
            l.remove(v)
        except ValueError:
            pass

    def get_bars(self, order_book_id, fields=None):
        try:
            s, e = self._index[order_book_id]
        except KeyError:
            six.print_(_(u"No data for {}").format(order_book_id))
            return

        if fields is None:
            # the first is date
            fields = self._table.names[1:]

        if len(fields) == 1:
            return self._converter.convert(fields[0], self._table.cols[fields[0]][s:e])

        # remove datetime if exist in fields
        self._remove_(fields, 'datetime')

        dtype = np.dtype([('datetime', np.uint64)] +
                         [(f, self._converter.field_type(f, self._table.cols[f].dtype))
                          for f in fields])
        result = np.empty(shape=(e - s, ), dtype=dtype)
        for f in fields:
            result[f] = self._converter.convert(f, self._table.cols[f][s:e])
        result['datetime'] = self._table.cols['date'][s:e]
        result['datetime'] *= 1000000

        return result

    def get_date_range(self, order_book_id):
        s, e = self._index[order_book_id]
        return self._table.cols['date'][s], self._table.cols['date'][e - 1]