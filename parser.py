# -*- coding: utf-8 -*-
from __future__ import (print_function, division, absolute_import, unicode_literals, )

from pyparsing import (
    Optional,
    Word,
    Literal,
    Keyword,
    OneOrMore,
    ZeroOrMore,
    Group,
    LineEnd,
    WordEnd,
    Suppress,
    Forward,
    ParserElement,
    CharsNotIn,
    QuotedString,
    quotedString,
    nestedExpr,
    removeQuotes,
)
from pyparsing import (printables, alphanums, cppStyleComment, )
from pyparsing import (ParseException, )


BASE_STRINGS = alphanums + "-" + "_"
BASE_WORDS = Word(BASE_STRINGS)
QUOTED_WORDS = quotedString.addParseAction(removeQuotes)
END_OF_WORDS = WordEnd(BASE_STRINGS)


LineSeparator = Suppress(Literal(';')).setResultsName('separator_token')
Comments = Optional(cppStyleComment.setResultsName('comment'))

NameDefinitions = BASE_WORDS.setResultsName('name')
ValDefinitions = OneOrMore(
    QUOTED_WORDS ^
    BASE_WORDS ^
    nestedExpr(opener='{', closer='}')
).setResultsName('value')
VarDefinitions = Group(
    NameDefinitions + END_OF_WORDS.copy() + ValDefinitions
)
OnlyVar = Word(printables)


# NestedVar = nestedExpr(opener='{', closer='}', content=VarDefinitions)
opener, closer = Literal('{'), Literal('}')
NestedVar = Forward()
_NestedContent = (
    VarDefinitions +
    CharsNotIn('{' + '}' + ParserElement.DEFAULT_WHITE_CHARS).setParseAction(lambda t: t[0].strip())
)
NestedVar << (
    Suppress(opener) +
    OneOrMore(NestedVar | _NestedContent) +
    Suppress(closer)
)
OptionsDefinitions = Group(
    Keyword('options').setResultsName('name') +
    NestedVar.copy().setResultsName('values')
)

ZoneDefinitions = Group(
    Keyword('zone').setResultsName('name') +
    QUOTED_WORDS.setResultsName('zone_name') +
    NestedVar.copy().setResultsName('values')
)

Expressions = OneOrMore(
    ZoneDefinitions |
    OptionsDefinitions |
    VarDefinitions
)



if __name__ == '__main__':
    from pyparsing import ParseResults
    # texts = io.open('', 'rt').read().replace('\n', '')
    # print(texts)
    p = OneOrMore(
        Comments +
        Expressions +
        LineSeparator
    )
    c = open('./named.conf').read()
    # parseFile('./testbase.conf')
    result = p.parseString(c)
    result = p.parseString(c, parseAll=True)
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
    # print(result[3]['values'])
    # print(result[3]['values'][0]['name'])
    # print(result[3]['values'][0]['value'])
    # print(result[3]['values'][1])
    # print(result[3]['values'][1])


# def hollerith():
#     '''Returns a parser for a FORTRAN Hollerith character constant.
#     '''
#     intExpr = pp.Word(pp.nums).setParseAction(lambda t: int(t[0]))
#     stringExpr = pp.Forward()
#     def countedParseAction(toks):
#         '''Closure to define the content of stringExpr.
#         '''
#         n = toks[0]
#         contents = pp.CharsNotIn('', exact=n)
#         stringExpr << (pp.Suppress(pp.CaselessLiteral('H')) + contents)
#         return None
#
#     intExpr.addParseAction(countedParseAction)
#     return (pp.Suppress(intExpr) + stringExpr)
