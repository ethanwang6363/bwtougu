#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pickle

from bwtougu.model.instrument import Instrument


class InstrumentStore(object):
    def __init__(self, f):
        with open(f, 'rb') as store:
            d = pickle.load(store)
        self._instruments = [Instrument(i) for i in d]

    def get_all_instruments(self):
        return self._instruments
