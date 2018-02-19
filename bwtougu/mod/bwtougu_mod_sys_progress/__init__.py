#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__config__ = {
    "show": False
}

def load_mod():
    from .mod import ProgressMod
    return ProgressMod()

