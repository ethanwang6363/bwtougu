#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import codecs
import yaml
import os

default_mod_config_path = os.path.join(os.path.dirname(__file__), '..', 'mod_config.yml')

def load_yaml(path):
    with codecs.open(path, encoding='utf-8') as f:
        return yaml.load(f)
    
def get_mod_conf():
    base = load_yaml(default_mod_config_path)
    return base
    
    
    