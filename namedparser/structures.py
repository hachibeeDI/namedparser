# -*- coding: utf-8 -*-
from __future__ import (print_function, division, absolute_import, unicode_literals, )


from pyparsing import ParseResults


class Include(dict):
    def __init__(self, parse_result):
        super(Include, self).__init__(name=parse_result['name'], value=parse_result['value'])

    def __str__(self):
        assert self['name'] == 'include'
        return 'include "{}";'.format(self['value'][0])

    def __repr__(self):
        return self.__str__()


StructuresDetection = {
    'include': Include,
}
