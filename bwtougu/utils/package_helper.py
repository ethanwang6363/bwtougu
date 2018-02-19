#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bwtougu.utils.logger import system_log

def import_mod(mod_name):
    try:
        from importlib import import_module
        return import_module(mod_name)
    except Exception as e:
        system_log.error("*" * 30)
        system_log.error("Mod Import Error: {}, error: {}", mod_name, e)
        system_log.error("*" * 30)
        raise
