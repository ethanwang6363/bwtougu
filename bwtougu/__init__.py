#!usr/bin/env python3
# -*- coding: utf-8 -*-
import pkgutil

from bwtougu.__main__ import cli
from bwtougu.api.api_base import export_as_api

__all__ = [
    '__version__',
    'version_info'
]

__version__ = pkgutil.get_data(__package__, 'VERSION.txt').decode('ascii').strip()

version_info = tuple(int(v) if v.isdigit() else v
                     for v in __version__.split('.'))

def test():
    print("hello world!")
    
if __name__ == '__main__':
    test()
