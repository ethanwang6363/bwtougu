#!/usr/bin/env python
# -*- coding: utf-8 -*-

import click
from bwtougu import cli

__config__ = {
    "stock_t1": True
}

def load_mod():
    from .mod import AccountMod
    return AccountMod()
