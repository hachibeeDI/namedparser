# -*- coding: utf-8 -*-
from __future__ import (print_function, division, absolute_import, unicode_literals, )

from os import path

from helper import unittest
from namedparser import parser
from namedparser import structures



class TestOptionsNode(unittest.TestCase):

    def setUp(self):
        with open(path.dirname(__file__) + '/resources/named.conf') as f:
            text = f.read()
        self.result = parser.Parser.parseString(text)
        self.option_node = self.result[1]  # line 0 is comment

    def test_option_defined_in_sample_resource(self):
        self.assertEqual(self.option_node.node_type, 'options')

    def test_has_minimum_requirement(self):
        require_node_types = (
            'directory',
            'check-names',
            'allow-recursion',
            'allow-query',
            'allow-query-cache',
            'allow-transfer',
            'max-cache-ttl',
            'min-retry-time',
            'max-acache-size',
            'max-journal-size',
            'version',
            'dnssec-enable',
            'dnssec-validation',
            'empty-zones-enable',
        )
        values_in_option = self.option_node.value
        values_not_contained = [req for req in require_node_types if req not in values_in_option]
        self.assertEqual(values_not_contained, [])

        invalid_node = parser.Parser.parseString('''
        options {
            directory "/var/na/named";
            check-names slave ignore;
        };
        ''')
        invalid_options_value = invalid_node[0].value
        values_not_contained = [req for req in require_node_types if req not in invalid_options_value]
        self.assertNotEqual(values_not_contained, [])

