# -*- coding: utf-8 -*-
from __future__ import (print_function, division, absolute_import, unicode_literals, )

import unittest

from namedparser import parser
from namedparser import structures


class TestTest(unittest.TestCase):

    def test_basic_vardefinition(self):
        text = '''
            directory "/var/na/named";
            aaa master;
            check-names slave ignore;
            include "named.local.conf";
        '''
        result = parser.Parser.parseString(text)
        self.assertEqual(result[0].name, 'directory')
        self.assertEqual(result[0].value, '/var/na/named')
        self.assertEqual(result[1].name, 'aaa')
        self.assertEqual(result[1].value.asList(), ['master'])
        self.assertEqual(result[2].name, 'check-names')
        self.assertEqual(result[2].target, 'slave')
        self.assertEqual(str(result[2]), 'check-names slave ignore;')
        include_expression = result[3]
        self.assertTrue(isinstance(include_expression, structures.Include))
        self.assertEqual(include_expression['name'], 'include')
        self.assertEqual(include_expression['value'], 'named.local.conf')
        self.assertEqual(str(include_expression), 'include "named.local.conf";')

    def test_option_definition(self):
        text = '''
        options {
            directory "/var/na/named";
            check-names slave ignore;
        };
        aaa master;
        '''
        result = parser.Parser.parseString(text)
        option_node = result[0]
        self.assertEqual(option_node.name, 'options')
        values_in_option = option_node['value']
        self.assertEqual(values_in_option.values[0].name, 'directory')
        self.assertEqual(values_in_option.values[0].value, '/var/na/named')


    def test_zone_definition(self):
        text = '''
        zone "zone_name" {
            directory "/var/na/named";
            check-names slave ignore;
        };
        aaa master;
        '''
        result = parser.Parser.parseString(text)
        zone_node = result[0]
        self.assertEqual(zone_node.name, 'zone')
        self.assertEqual(zone_node.zone_name, 'zone_name')
        values_in_zone = zone_node['value']
        self.assertEqual(values_in_zone.values[0].name, 'directory')
        self.assertEqual(values_in_zone.values[0].value, '/var/na/named')
        self.assertEqual(values_in_zone.values[1].name, 'check-names')
        self.assertEqual(values_in_zone.values[1].target, 'slave')
        self.assertEqual(values_in_zone.values[1].value, 'ignore')

    def pass_(self):
        from pyparsing import ParseResults
        c = open('./testbase.conf').read()
        # parseFile('./testbase.conf')
        result = parser.Parser.parseString(c)
        # result = p.parseString(c, parseAll=True)
        for r in [r for r in result if isinstance(r, ParseResults)]:
            print('- = - = - = - = - = -')
            name = r['name']
            print('section: {}'.format(name))
            if name == 'options':
                values = r['values']
                print('values: {}'.format(r['values']))
                for v in [v for v in values if isinstance(v, ParseResults)]:
                    print('  {}: {}'.format(v['name'], v['value']))
            elif name == 'zone':
                print('zone_name: {}'.format(r['zone_name']))
                values = r['values']
                print('values: {}'.format(r['values']))
                for v in [v for v in values if isinstance(v, ParseResults)]:
                    print('  {}: {}'.format(v['name'], v['value']))
            else:
                print('value: {}'.format(r['value']))
