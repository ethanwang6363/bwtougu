#!/usr/bin/env python
# -*- coding: utf-8 -*-

import six


def property_repr(inst):
    # return pformat(properties(inst))
    return "%s(%s)" % (inst.__class__.__name__, properties(inst))


def slots_repr(inst):
    # return pformat(slots(inst))
    return "%s(%s)" % (inst.__class__.__name__, slots(inst))


def dict_repr(inst):
    # return pformat(inst.__dict__)
    return "%s(%s)" % (
        inst.__class__.__name__, {k: v for k, v in six.iteritems(inst.__dict__) if k[0] != "_"})


def properties(inst):
    result = {}
    for cls in inst.__class__.mro():
        abandon_properties = getattr(cls, '__abandon_properties__', [])
        for varname in iter_properties_of_class(cls):
            if varname[0] == "_":
                continue
            if varname in abandon_properties:
                # 如果 设置了 __abandon_properties__ 属性，则过滤其中的property，不输出相关内容
                continue
            # FIXME: 这里getattr在iter_properties_of_class中掉用过了，性能比较差，可以优化
            tmp = getattr(inst, varname)
            if varname == "positions":
                tmp = list(tmp.keys())
            if hasattr(tmp, '__simple_object__'):
                result[varname] = tmp.__simple_object__()
            else:
                result[varname] = tmp
    return result


def slots(inst):
    result = {}
    for slot in inst.__slots__:
        result[slot] = getattr(inst, slot)
    return result


def iter_properties_of_class(cls):
    for varname in vars(cls):
        value = getattr(cls, varname)
        if isinstance(value, property):
            yield varname
