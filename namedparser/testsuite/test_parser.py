# -*- coding: utf-8 -*-
from __future__ import (division, absolute_import, )

from os import path
from helper import unittest

from namedparser import Parser
from namedparser import structures


class TestBase(unittest.TestCase):
    def setUp(self):
        with open(path.dirname(__file__) + '/resources/named.conf') as f:
            text = f.read()
        self.prepared_named = Parser.parse_string(text)

    def test_basic_vardefinition(self):
        text = '''
            directory "/var/na/named";
            aaa master;
            check-names slave ignore;
            include "named.local.conf";
        '''
        result = Parser.parse_string(text)
        self.assertEqual(result[0].node_type, 'directory')
        self.assertEqual(result[0].value, '/var/na/named')

        self.assertIsInstance(result[1], structures.UnknowNode)
        self.assertEqual(result[1].node_type, 'aaa')
        self.assertEqual(result[1].value, 'master')

        self.assertEqual(result[2].node_type, 'check-names')
        self.assertEqual(result[2].target, 'slave')
        self.assertEqual(str(result[2]), 'check-names slave ignore;')

        include_expression = result[3]
        self.assertTrue(isinstance(include_expression, structures.Include))
        self.assertEqual(include_expression['node_type'], 'include')
        self.assertEqual(include_expression['value'], 'named.local.conf')
        self.assertEqual(str(include_expression), 'include "named.local.conf";')

    def test_acl_vardefinition(self):
        text = '''
        acl "acl_test" {
            1.1.1.1;
            1.1.1.2;
            1.1.1.3;
            1.1.1.4;
        };
        aaa master;
        '''
        result = Parser.parse_string(text)
        acl_node = result[0]
        self.assertEqual(acl_node.node_type, 'acl')
        self.assertEqual(acl_node.name, 'acl_test')
        values_in_acl = acl_node['value']
        self.assertEqual(values_in_acl.values[0], '1.1.1.1')
        self.assertEqual(values_in_acl.values[1], '1.1.1.2')
        self.assertEqual(
            str(values_in_acl).replace('\n', '').replace(' ', ''),
            '''{1.1.1.1;1.1.1.2;1.1.1.3;1.1.1.4;}'''
        )

    def test_search_node_from_groups(self):
        result = self.prepared_named
        option_node = result[1]
        self.assertEqual(option_node.node_type, 'options')
        values_in_option = option_node.value
        self.assertIsInstance(values_in_option, structures.DefinitionsContainer)
        check_names_nodes = list(values_in_option.search('check-names'))
        self.assertEqual(check_names_nodes[0].target, 'master')

    def test_search_nodes(self):
        result = self.prepared_named
        options = result.search('options')
        self.assertEqual(options[0].node_type, 'options')
        _ = result.search('foo')
        self.assertEqual(_, [])


class TestOptionsNode(unittest.TestCase):

    def test_option_definition(self):
        text = '''
        options {
            directory "/var/na/named";
            check-names slave ignore;
        };
        aaa master;
        '''
        result = Parser.parse_string(text)
        option_node = result[0]
        self.assertEqual(option_node.node_type, 'options')
        values_in_option = option_node['value']
        self.assertEqual(values_in_option.values[0].node_type, 'directory')
        self.assertEqual(values_in_option.values[0].value, '/var/na/named')

    def test_stringfy(self):
        text = '''
        options {
            directory "/var/na/named";
            check-names slave ignore;
        };
        aaa master;
        '''
        result = Parser.parse_string(text)
        option_node = result[0]
        self.assertEqual(
            str(option_node).replace(' ', '').replace('\n', ''),
            '''options {
                directory "/var/na/named";
                check-names slave ignore;
            };'''.replace(' ', '').replace('\n', '')
        )



class TestZoneNode(unittest.TestCase):

    def test_zone_definition(self):
        text = '''
        zone "zone_name" {
            directory "/var/na/named";
            check-names slave ignore;
        };
        aaa master;
        '''
        result = Parser.parse_string(text)
        zone_node = result[0]
        self.assertEqual(zone_node.node_type, 'zone')
        self.assertEqual(zone_node.name, 'zone_name')
        values_in_zone = zone_node['value']
        self.assertEqual(values_in_zone.values[0].node_type, 'directory')
        self.assertEqual(values_in_zone.values[0].value, '/var/na/named')
        self.assertEqual(values_in_zone.values[1].node_type, 'check-names')
        self.assertEqual(values_in_zone.values[1].target, 'slave')
        self.assertEqual(values_in_zone.values[1].value, 'ignore')


class TestSuitably(unittest.TestCase):
    pass
    # def test_megrep(self):
    #     from pyparsing import ParseResults
    #     c = open(path.dirname(__file__) + '/resources/named.conf').read()
    #     # parseFile('./testbase.conf')
    #     result = parser.Parser.parse_string(c)
    #     # result = p.parse_string(c, parseAll=True)
    #     for r in [r for r in result if isinstance(r, ParseResults)]:
    #         print('- = - = - = - = - = -')
    #         name = r['node_type']
    #         print('section: {}'.format(name))
    #         if name == 'options':
    #             values = r['value']
    #             print('value: {}'.format(r['value']))
    #             for v in [v for v in values if not isinstance(v, basestring)]:
    #                 print('  {}: {}'.format(v['node_type'], v['value']))
    #         elif name == 'zone':
    #             print("zone's name: {}".format(r['name']))
    #             values = r['value']
    #             print('value: {}'.format(r['value']))
    #             for v in [v for v in values if not isinstance(v, basestring)]:
    #                 print('  {}: {}'.format(v['node_type'], v['value']))
    #         else:
    #             print('value: {}'.format(r['value']))
    #     self.assertTrue(True)  # expect no error
