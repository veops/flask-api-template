# -*- coding:utf-8 -*- 

from typing import Set

import six
from flask import current_app


class BaseEnum(object):
    _ALL_ = set()  # type: Set[str]

    @classmethod
    def is_valid(cls, item):
        return item in cls.all()

    @classmethod
    def all(cls):
        if not cls._ALL_:
            cls._ALL_ = {
                getattr(cls, attr)
                for attr in dir(cls)
                if not attr.startswith("_") and not callable(getattr(cls, attr))
            }
        return cls._ALL_


def get_page(page):
    try:
        page = int(page)
    except (TypeError, ValueError):
        page = 1
    return page if page >= 1 else 1


def get_page_size(page_size):
    if page_size == "all":
        return page_size

    try:
        page_size = int(page_size)
    except (ValueError, TypeError):
        page_size = current_app.config.get("DEFAULT_PAGE_COUNT")
    return page_size if page_size >= 1 else current_app.config.get("DEFAULT_PAGE_COUNT")


def handle_bool_arg(arg):
    if arg in current_app.config.get("BOOL_TRUE"):
        return True
    return False


def handle_arg_list(arg):
    if isinstance(arg, (list, dict)):
        return arg

    if arg == 0:
        return [0]

    if not arg:
        return []

    if isinstance(arg, (six.integer_types, float)):
        return [arg]
    return list(filter(lambda x: x != "", arg.strip().split(","))) if isinstance(arg, six.string_types) else arg
