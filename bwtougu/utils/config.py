#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import locale
import codecs

import pandas as pd
import yaml
import simplejson as json
import six


from bwtougu.const import RUN_TYPE
from bwtougu.utils.dict_func import deep_update
from bwtougu.utils import RqAttrDict, logger
from bwtougu.utils.i18n import gettext as _, localization
from bwtougu.utils.py2 import to_utf8

rqalpha_path = "~/.rqalpha"

default_config_path = os.path.join(os.path.dirname(__file__), '..', 'config.yml')
default_mod_config_path = os.path.join(os.path.dirname(__file__), '..', 'mod_config.yml')
default_user_mod_config_path = os.path.join(os.path.dirname(__file__), '..', 'mod_config.yml')

def user_mod_conf_path():
    # return os.path.join(os.path.expanduser(rqalpha_path), 'mod_config.yml')
    return default_user_mod_config_path

def load_yaml(path):
    with codecs.open(path, encoding='utf-8') as f:
        return yaml.load(f)
    
def get_mod_conf():
    base = load_yaml(default_mod_config_path)
    return base

def default_config():
    base = load_yaml(default_config_path)
    base['base']['source_code'] = None
    mod = load_yaml(default_mod_config_path)
    deep_update(mod, base)
    return base

def parse_config(config_args, config_path=None, click_type=False, source_code=None, user_funcs=None):
    conf = default_config()
    if config_path is not None:
        deep_update(load_yaml(config_path), conf)

    if 'base__strategy_file' in config_args and config_args['base__strategy_file']:
        # FIXME: ugly, we need this to get code
        conf['base']['strategy_file'] = config_args['base__strategy_file']
    elif ('base' in config_args and 'strategy_file' in config_args['base'] and
          config_args['base']['strategy_file']):
        conf['base']['strategy_file'] = config_args['base']['strategy_file']

    if click_type:
        for k, v in six.iteritems(config_args):
            if v is None:
                continue
            if k == 'base__accounts' and not v:
                continue

            key_path = k.split('__')
            sub_dict = conf
            for p in key_path[:-1]:
                if p not in sub_dict:
                    sub_dict[p] = {}
                sub_dict = sub_dict[p]
            sub_dict[key_path[-1]] = v
    else:
        deep_update(config_args, conf)

    config = RqAttrDict(conf)

    set_locale(config.extra.locale)

    def _to_date(v):
        return pd.Timestamp(v).date()

    config.base.start_date = _to_date(config.base.start_date)
    config.base.end_date = _to_date(config.base.end_date)

    if config.base.data_bundle_path is None:
        config.base.data_bundle_path = os.path.join(os.path.expanduser(rqalpha_path), "bundle")

    config.base.run_type = parse_run_type(config.base.run_type)
    config.base.accounts = parse_accounts(config.base.accounts)
    # config.base.init_positions = parse_init_positions(config.base.init_positions)
    # config.base.persist_mode = parse_persist_mode(config.base.persist_mode)

    if config.extra.context_vars:
        if isinstance(config.extra.context_vars, six.string_types):
            config.extra.context_vars = json.loads(to_utf8(config.extra.context_vars))

#    if config.base.frequency == "1d":
#        logger.DATETIME_FORMAT = "%Y-%m-%d"

    return config


def parse_accounts(accounts):
    a = {}
    if isinstance(accounts, tuple):
        accounts = {account_type: starting_cash for account_type, starting_cash in accounts}

    for account_type, starting_cash in six.iteritems(accounts):
        if starting_cash is None:
            continue
        starting_cash = float(starting_cash)
        a[account_type.upper()] = starting_cash
    if len(a) == 0:
        raise RuntimeError(_(u"None account type has been selected."))
    return a


def parse_run_type(rt_str):
    assert isinstance(rt_str, six.string_types)
    mapping = {
        "b": RUN_TYPE.BACKTEST,
        "p": RUN_TYPE.PAPER_TRADING,
        "r": RUN_TYPE.LIVE_TRADING,
    }
    try:
        return mapping[rt_str]
    except KeyError:
        raise RuntimeError(_(u"unknown run type: {}").format(rt_str))


def set_locale(lc):
    # FIXME: It should depends on the system and locale config
    try:
        locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
        locale.setlocale(locale.LC_CTYPE, "en_US.UTF-8")
        os.environ['TZ'] = 'Asia/Shanghai'
    except Exception as e:
        if os.name != 'nt':
            raise
    localization.set_locale([lc])

def dump_config(config_path, config, dumper=yaml.Dumper):
    dirname = os.path.dirname(config_path)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    with codecs.open(config_path, mode='w', encoding='utf-8') as stream:
        stream.write(to_utf8(yaml.dump(config, Dumper=dumper)))