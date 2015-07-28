# -*- coding: utf-8 -*-
from __future__ import (division, absolute_import, )

from functools import reduce
from pyparsing import ParseResults

from .parser import _Parser
from .structures import Results


__all__ = (
    'Parser',
)


def _snake_to_camel(text):
    '''
    >>> _snake_to_camel('_snake_to_camel')
    u'SnakeToCamel'
    >>> _snake_to_camel('parse_file')
    u'parseFile'
    '''
    letters = list(text)

    def _conv(l1, l2):
        if l1[-1] == '_':
            return l1.replace('_', '') + l2.upper()
        return l1 + l2
    return ''.join(
        reduce(_conv, letters)
    )


class P(object):
    ''' you can call Parser methods not only camelCase but also snake_case '''

    def __getattr__(self, name):
        name_of_calling = _snake_to_camel(name)
        ret = getattr(_Parser, name_of_calling)
        if name_of_calling.startswith('parse'):
            return lambda *args: Results(ret(*args, parseAll=True))
        return ret


Parser = P()
