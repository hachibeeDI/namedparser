# -*- coding: utf-8 -*-
from __future__ import (division, absolute_import, )

from os import path

from helper import unittest
from namedparser import Parser
from namedparser import structures



class TestOptionsNode(unittest.TestCase):
    REQUIRE_NODE_TYPES = (
        'directory',
        'check-names',
        'allow-recursion',
        'allow-query',
        'allow-query-cache',
        'allow-transfer',
        'max-cache-ttl',
        'min-retry-time',
        'max-acache-size',
        'max-cache-size',
        'max-journal-size',
        'version',
        'dnssec-enable',
        'dnssec-validation',
        'empty-zones-enable',
    )

    def setUp(self):
        with open(path.dirname(__file__) + '/resources/named.conf') as f:
            text = f.read()
        self.result = Parser.parse_string(text)
        self.option_node = self.result[1]  # line 0 is comment

    def test_option_defined_in_sample_resource(self):
        self.assertEqual(self.option_node.node_type, 'options')

    def test_has_minimum_requirement(self):
        values_in_option = self.option_node.value
        values_not_contained = [req for req in TestOptionsNode.REQUIRE_NODE_TYPES if req not in values_in_option]
        self.assertEqual(values_not_contained, [])

        invalid_node = Parser.parse_string('''
        options {
            directory "/var/na/named";
            check-names slave ignore;
            hoge fooo;
        };''')
        invalid_options_value = invalid_node[0].value
        values_not_contained = [req for req in TestOptionsNode.REQUIRE_NODE_TYPES if req not in invalid_options_value]
        self.assertNotEqual(values_not_contained, [])

    def test_hasnot_uninvited_values(self):
        values_in_option = self.option_node.value
        values_not_contained = [var for var in values_in_option if var.node_type not in TestOptionsNode.REQUIRE_NODE_TYPES]
        self.assertEqual(values_not_contained, [])

        invalid_node = Parser.parse_string('''
        options {
            directory "/var/na/named";
            check-names slave ignore;
            hoge fooo;
        };''')
        invalid_options_value = invalid_node[0].value
        values_not_contained = [
            var for var in invalid_options_value
            if var.node_type not in TestOptionsNode.REQUIRE_NODE_TYPES
        ]
        self.assertNotEqual(values_not_contained, [])


class TestZoneNode(unittest.TestCase):
    REQUIRE_NODE_TYPES = (
        'type',
        'max-journal-size',
    )
    VALID_NODE_TYPES = REQUIRE_NODE_TYPES + (
        'masters',  # zonetypeがslaveのとき
        'forwarders',  # zonetypeがforwardのとき
        'file',  # zonetypeがforward以外のとき
        'also-notify',  # zonetypeがmasterのとき
        'allow-update',  # zonetypeがmasterのとき
        'allow-transfer',  # allow-transferが空じゃなければ
        'allow-query',  # allow-queryが空じゃなければ
    )

    def setUp(self):
        self.result = Parser.parse_file(path.dirname(__file__) + '/resources/named.conf')

    def test_has_minimum_requirement(self):
        zones = self.result.search('zone')
        first_node = zones[0]
        values_not_contained = [
            req_type for req_type in TestZoneNode.REQUIRE_NODE_TYPES
            if req_type not in first_node.value
        ]
        self.assertEqual(values_not_contained, [])
