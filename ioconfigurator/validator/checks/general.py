import re
from typing import Callable

from ioconfigurator.parsers.parser import model


__all__ = ['checks']


# def _var_name(s: model.ParsedLine):
#     """невозможное название переменной"""
#     if s.var is not None and s.var != '' and not bool(re.search('^[a-zA-Z](?:_?[a-zA-Z0-9]+)*$', s.var)):
#         raise TypeError(s.var)


def _signal_name(s: model.ParsedLine):
    pass


def _module_type(s: model.ParsedLine):
    pass


def _module_capacity(s: model.ParsedLine):
    pass


def _module_duplicate_channel(s: model.ParsedLine):
    pass


def checks() -> tuple[Callable[[model.ParsedLine], None], ...]:
    # return _var_name, _signal_name, _module_type, _module_capacity, _module_duplicate_channel
    return _signal_name, _module_type, _module_capacity, _module_duplicate_channel
