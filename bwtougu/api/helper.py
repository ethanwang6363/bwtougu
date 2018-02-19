#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bwtougu.api import api_base


def get_apis():
    apis = {name: getattr(api_base, name) for name in api_base.__all__}
    # apis.update((name, getattr(api_extension, name)) for name in api_extension.__all__)
    return apis