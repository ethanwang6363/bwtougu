#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bwtougu.interface import AbstractMod

class ProgressMod(AbstractMod):
    def __init__(self):
        self._show = False
        self._progress_bar = None
        self._trading_length = 0
        self._env = None

    def start_up(self, env, mod_config):
        self._show = mod_config.show
        self._env = env

    def _init(self, event):
        pass

    def _tick(self, event):
        pass

    def tear_down(self, success, exception=None):
        if self._show:
            self._progress_bar.render_finish()
