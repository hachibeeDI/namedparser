# -*- coding: utf-8 -*-
from __future__ import (print_function, division, absolute_import, unicode_literals, )

from os import path
from helper import unittest

from namedparser import Parser
from namedparser import structures


class TestBase(unittest.TestCase):

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
            '''{1.1.1.1;1.1.1.2;1.1.1.3;1.1.1.4;};'''
        )

    def test_search_node_from_groups(self):
        text = open(path.dirname(__file__) + '/resources/named.conf').read()
        result = Parser.parse_string(text)
        option_node = result[1]
        self.assertEqual(option_node.node_type, 'options')
        values_in_option = option_node.value
        self.assertIsInstance(values_in_option, structures.DefinitionsContainer)
        check_names_nodes = list(values_in_option.search('check-names'))
        self.assertEqual(check_names_nodes[0].target, 'master')

    @unittest.expectedFailure
    def test_search_nodes(self):
        with open(path.dirname(__file__) + '/resources/named.conf') as f:
            text = f.read()
        result = Parser.parse_string(text)
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



valid_node_types = '''
riteLn( io::str( format( "// %s created by NamedConfCreator" )
    riteLn( "options {" );
    riteLn( "directory \"/var/named\";", 2 );
    riteLn( io::str( format( "directory \"%s\";" ) % strZoneDir ), 2 );
    riteLn( "check-names master ignore;" );
    riteLn( "check-names slave ignore;" );
    riteLn( "check-names response ignore;" );
    WriteLn( MakeAddressBlock( "allow-recursion", strFormRecursion, false ) );
    WriteLn( MakeAddressBlock( "allow-query", strFormQuery, true ) );
    WriteLn( MakeAddressBlock( "allow-query-cache", strFormQueryCache, false ) );
    WriteLn( "allow-transfer { 127.0.0.1; };" );
    WriteLn( "max-cache-ttl  3600000;" );
    WriteLn( "min-retry-time  50;" );
    WriteLn( io::str( format( "max-acache-size %s;" )
    WriteLn( io::str( format( "max-cache-size %s;" )
    WriteLn( "max-journal-size 100k;" );
    WriteLn( io::str( format( "version \"%s\";" )
    WriteLn("listen-on-v6{");
    WriteLn( io::str( format("	any;") ) );
    WriteLn(io::str(format("	%s;") % strIPv6Addr0));
    WriteLn(io::str(format("	%s;") % strIPv6Addr1));
    WriteLn("};");
WriteLn("dnssec-enable yes;");
WriteLn("dnssec-enable no;");
WriteLn("dnssec-validation yes;");
WriteLn("dnssec-validation no;");
WriteLn("empty-zones-enable yes;");
WriteLn( "forwarders {", 2 );
WriteLn( io::str( format( "%s" ) % strForwarders ), 4 );
WriteLn( "};", 2 );
WriteLn( MakeAddressBlock( "forwarders", strForwarders, false ) );
WriteLn( "};");
WriteLn("trusted-keys {");
WriteLn(io::str(format("	\"%s\" 257 3 %d \"%s\";")
WriteLn("};");
WriteLn( io::str( format( "include \"%s\";" )
WriteLn( "include \"fixedpart-named\";" );
WriteLn( "include \"named-rndc.conf\";" );


src/soliton/libnddns/nadns/src/ConfCreator.cpp|376 col 2| WriteLn( io::str( format( "zone \"%s\" {" ) % strZoneName ) );
src/soliton/libnddns/nadns/src/ConfCreator.cpp|388 col 2| WriteLn( io::str( format( "type %s;" ) %  strZoneType ), 2 );
src/soliton/libnddns/nadns/src/ConfCreator.cpp|390 col 9| WriteLn( "max-journal-size 100k;" );
src/soliton/libnddns/nadns/src/ConfCreator.cpp|394 col 3| WriteLn( MakeAddressBlock( "masters", strMasters, false ) );
src/soliton/libnddns/nadns/src/ConfCreator.cpp|400 col 3| WriteLn( MakeAddressBlock( "forwarders", strForwarders, false ) );
src/soliton/libnddns/nadns/src/ConfCreator.cpp|409 col 3| WriteLn( io::str( format( "file \"%s\";" ) % strZoneFileName ), 2 );
src/soliton/libnddns/nadns/src/ConfCreator.cpp|417 col 17| WriteLn( "also-notify port 954 { 127.0.0.1; };" );
src/soliton/libnddns/nadns/src/ConfCreator.cpp|421 col 3| WriteLn( MakeAddressBlock( "allow-update", strAllowUpdate, true ) );
src/soliton/libnddns/nadns/src/ConfCreator.cpp|436 col 3| WriteLn( MakeAddressBlock( "allow-transfer", strAllowTransfer ) );
src/soliton/libnddns/nadns/src/ConfCreator.cpp|444 col 3| WriteLn( MakeAddressBlock( "allow-query", strAllowQuery ) );
src/soliton/libnddns/nadns/src/ConfCreator.cpp|447 col 2| WriteLn( "};" );
src/soliton/libnddns/nadns/src/ConfCreator.cpp|581 col 3| WriteLn( io::str( format( "%s %s" )
src/soliton/libnddns/nadns/src/ConfCreator.cpp|605 col 3| WriteLn( boost::io::str( boost::format( "$TTL %d" ) % pxRecord->nTtl )
src/soliton/libnddns/nadns/src/ConfCreator.cpp|607 col 3| WriteLn( pxRecord->ZoneFileString(), 0 );
src/soliton/libnddns/nadns/src/ConfCreator.cpp|612 col 3| WriteLn( pxRecord->String(), 0 );
src/soliton/libnddns/nadns/src/ConfCreator.cpp|653 col 2| WriteLn( io::str( format( "$TTL %d" ) % pxRecord->nTtl ) );
src/soliton/libnddns/nadns/src/ConfCreator.cpp|659 col 2| WriteLn( io::str( format( "@ IN SOA %s %s (" )
src/soliton/libnddns/nadns/src/ConfCreator.cpp|668 col 2| WriteLn( io::str( format( "%d" ) % pxRecord->rData.dwSerial ), 2 );
src/soliton/libnddns/nadns/src/ConfCreator.cpp|670 col 2| WriteLn( io::str( format( "%d" ) % pxRecord->rData.dwRefresh ), 2 );
src/soliton/libnddns/nadns/src/ConfCreator.cpp|671 col 2| WriteLn( io::str( format( "%d" ) % pxRecord->rData.dwRetry ), 2 );
src/soliton/libnddns/nadns/src/ConfCreator.cpp|673 col 2| WriteLn( io::str( format( "%d" ) % pxRecord->rData.dwExpire ), 2 );
src/soliton/libnddns/nadns/src/ConfCreator.cpp|674 col 2| WriteLn( io::str( format( "%d" ) % pxRecord->rData.dwMinimum ), 2 );
src/soliton/libnddns/nadns/src/ConfCreator.cpp|676 col 2| WriteLn( ")" );
src/soliton/libnddns/nadns/src/ConfCreator.cpp|685 col 2| WriteLn( io::str( format( "%s IN %s      %s" )
'''
