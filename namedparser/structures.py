# -*- coding: utf-8 -*-
from __future__ import (print_function, division, absolute_import, unicode_literals, )


from pyparsing import ParseResults


class ValueDefinitions(object):
    def __str__(self):
        return '{} {};'.format(self['node_type'], self['value'])

    def __repr__(self):
        return self.__str__()

    def asList(self):
        return [self['node_type'], self['value']]


class QuotedValuePossesiable(ValueDefinitions):
    def __str__(self):
        return '{} "{}";'.format(self['node_type'], self['value'])


class EasyAcceesser(object):
    def __getattr__(self, name):
        return self[name]


# =================


class UnknowSentence(ValueDefinitions, EasyAcceesser, dict):
    def __init__(self, parse_result):
        assert 'node_type' in parse_result and 'value' in parse_result
        super(UnknowSentence, self).__init__(node_type=parse_result['node_type'], value=parse_result['value'][0])


class Include(QuotedValuePossesiable, EasyAcceesser, dict):
    def __init__(self, parse_result):
        super(Include, self).__init__(node_type=parse_result['node_type'], value=parse_result['value'][0])


class Directory(QuotedValuePossesiable, EasyAcceesser, dict):
    def __init__(self, parse_result):
        super(Directory, self).__init__(node_type=parse_result['node_type'], value=parse_result['value'][0])


class CheckName(ValueDefinitions, EasyAcceesser, dict):
    def __init__(self, parse_result):
        super(CheckName, self).__init__(
            node_type=parse_result['node_type'],
            target=parse_result['value'][0],
            value=parse_result['value'][1],
        )

    def __str__(self):
        return '{} {} {};'.format(self['node_type'], self['target'], self['value'], )

    def asList(self):
        return [self['node_type'], self['target'], self['value']]


class DefinitionsContainer(object):
    '''
    :warning:
        the handler of setParseAction should not return type of list.
    '''

    def __init__(self, var):
        self.values = var

    def __iter__(self):
        return self.values

    def next(self):
        return self.values.next()

    def __str__(self):
        return '\n'.join(str(v) for v in self.values)


class ValueLists(object):
    def __init__(self, var):
        self.values = var

    def __iter__(self):
        return self.values

    def next(self):
        return self.values.next()

    def __str__(self):
        return ';\n'.join(str(v) for v in self.values) + ';'


StructuresDetection = {
    'include': Include,
    'directory': Directory,
    'check-names': CheckName,
}
