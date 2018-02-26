#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
import traceback
import logbook
import better_exceptions
import os
from logbook import Logger, TimedRotatingFileHandler
from logbook.more import ColorizedStderrHandler

logbook.set_datetime_format("local")


# patch warn
logbook.base._level_names[logbook.base.WARNING] = 'WARN'


# better_exceptions hot patch
def format_exception(exc, value, tb):
    formatted, colored_source = better_exceptions.format_traceback(tb)

    if not str(value) and exc is AssertionError:
        value.args = (colored_source,)
    title = traceback.format_exception_only(exc, value)
    title = title[0].strip()
    full_trace = u'Traceback (most recent call last):\n{}{}\n'.format(formatted, title)

    return full_trace


better_exceptions.format_exception = format_exception


__all__ = [
    "user_log",
    "system_log",
]


DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"


def user_std_handler_log_formatter(record, handler):
    dt = datetime.now().strftime(DATETIME_FORMAT)

    log = "[{dt}][{level}]:{channel}:[{filename}:{lineno}][{func_name}] {msg}".format(
        dt=dt,
        level=record.level_name,                      # 日志等级
        channel=record.channel,
        filename=os.path.split(record.filename)[-1],  # 文件名
        lineno=record.lineno,                         # 行号
        func_name=record.func_name,                   # 函数名
        msg=record.message,
    )
    return log


user_std_handler = ColorizedStderrHandler(bubble=True)
user_std_handler.formatter = user_std_handler_log_formatter


# 日志路径，在主工程下生成log目录
LOG_DIR = os.path.join('log')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# 打印到文件句柄
user_file_handler = TimedRotatingFileHandler(os.path.join(LOG_DIR, '%s.log' % 'rqalpha'), date_format='%Y%m%d', bubble=True)
user_file_handler.formatter = user_std_handler_log_formatter

# loggers
# 用户代码logger日志
user_log = Logger("user_log")

# 系统日志
system_log = Logger("system_log")


def init_logger():
    system_log.handlers = []
    system_log.handlers.append(user_std_handler)

    user_log.handlers = []


def user_print(*args, **kwargs):
    sep = kwargs.get("sep", " ")
    end = kwargs.get("end", "")

    message = sep.join(map(str, args)) + end

    user_log.info(message)


init_logger()
