# -*- coding: utf-8 -*-
from __future__ import (print_function, division, absolute_import, unicode_literals, )

from helper import unittest


class TestOptionsNode(unittest.TestCase):

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
        self.assertEqual(option_node.node_type, 'options')
        values_in_option = option_node['value']
        self.assertEqual(values_in_option.values[0].node_type, 'directory')
        self.assertEqual(values_in_option.values[0].value, '/var/na/named')
