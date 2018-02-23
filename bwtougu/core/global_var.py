#!/usr/bin/env python
# -*- coding: utf-8 -*-


import six
import pickle
from bwtougu.utils.logger import system_log


class GlobalVars(object):
    def get_state(self):
        dict_data = {}
        for key, value in six.iteritems(self.__dict__):
            try:
                dict_data[key] = pickle.dumps(value)
            except Exception as e:
                system_log.exception("g.{} can not pickle", key)
                system_log.warn("g.{} can not pickle", key)
        return pickle.dumps(dict_data)

    def set_state(self, state):
        dict_data = pickle.loads(state)
        for key, value in six.iteritems(dict_data):
            try:
                self.__dict__[key] = pickle.loads(value)
                system_log.debug("restore g.{} {}", key, type(self.__dict__[key]))
            except Exception as e:
                system_log.exception("g.{} can not restore", key)
                system_log.warn("g.{} can not restore", key)