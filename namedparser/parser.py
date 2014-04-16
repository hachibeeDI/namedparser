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
    delimitedList,
    removeQuotes,
)
from pyparsing import (alphanums, cppStyleComment, )
from pyparsing import (ParseResults, )
from pyparsing import (ParseException, )

from .structures import (
    StructuresDetection,
    UnknowSentence,
    DefinitionsContainer,
    ValueLists,
)


BASE_STRINGS = alphanums + "-" + "_"
NETWORK_STRINGS = alphanums + "-" + "_" + '.'  # 適時調整
BASE_WORDS = Word(BASE_STRINGS)
QUOTED_WORDS = quotedString.addParseAction(removeQuotes)
END_OF_WORDS = WordEnd(BASE_STRINGS)


LineSeparator = Suppress(Literal(';')).setResultsName('separator_token')
Comments = Optional(cppStyleComment.setResultsName('comment'))
opener, closer = Literal('{'), Literal('}')

WORD_LIST = (
    opener.suppress() +
    delimitedList(Word(NETWORK_STRINGS), delim=';') +
    LineSeparator.suppress() +
    closer.suppress()
).setParseAction(lambda s, l, t: ValueLists(t))

NameDefinitions = BASE_WORDS.setResultsName('node_type')
ValDefinitions = OneOrMore(
    QUOTED_WORDS ^
    BASE_WORDS ^
    QuotedString('{', multiline=True, endQuoteChar='}').setParseAction(lambda t: t[0].strip())
).setResultsName('value')


def expression_type_detection(st, location_of__matching_substring, toks):
    var = toks[0]
    cls = StructuresDetection.get(var['node_type'], UnknowSentence)
    # if cls is None:
    #     return toks
    v = cls(var)
    return v

VarDefinitions = Group(
    NameDefinitions + ValDefinitions
).setParseAction(expression_type_detection)


def expression_type_detection_in_nestedvalues(st, loc, toks):
    contents = [t for t in toks if not (isinstance(t, basestring) or t == ';')]
    return DefinitionsContainer(contents)
NestedVar = Forward().setParseAction(expression_type_detection_in_nestedvalues)
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
    Keyword('options').setResultsName('node_type') +
    NestedVar.copy().setResultsName('value')
).setResultsName('option-node')

ZoneDefinitions = Group(
    Keyword('zone').setResultsName('node_type') +
    QUOTED_WORDS.setResultsName('name') +
    NestedVar.copy().setResultsName('value')
).setResultsName('zone-node')

AclDefinitions = Group(
    Keyword('acl').setResultsName('node_type') +
    QUOTED_WORDS.copy().setResultsName('name') +
    WORD_LIST.copy().setResultsName('value')
)


Expressions = OneOrMore(
    ZoneDefinitions |
    OptionsDefinitions |
    AclDefinitions |
    VarDefinitions
)

Parser = OneOrMore(
        Comments +
        Expressions +
        LineSeparator
    )
