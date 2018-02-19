#!/usr/bin/env python
# -*- utf-8 -*-
import codecs

from bwtougu.interface import AbstractStrategyLoader
from bwtougu.utils.strategy_loader_help import compile_strategy

class FileStrategyLoader(AbstractStrategyLoader):
    def __init__(self, strategy_file_path):
        self._strategy_file_path = strategy_file_path

    def load(self, scope):
        with codecs.open(self._strategy_file_path, encoding="utf-8") as f:
            source_code = f.read()

        return compile_strategy(source_code, self._strategy_file_path, scope)


class SourceCodeStrategyLoader(AbstractStrategyLoader):
    def __init__(self, code):
        self._code = code

    def load(self, scope):
        return compile_strategy(self._code, "strategy.py", scope)