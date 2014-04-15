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
from pyparsing import (printables, alphanums, cppStyleComment, )
from pyparsing import (ParseException, )


BASE_STRINGS = alphanums + "-" + "_"
BASE_WORDS = Word(BASE_STRINGS)
QUOTED_WORDS = quotedString.addParseAction(removeQuotes)
END_OF_WORDS = WordEnd(BASE_STRINGS)


LineSeparator = Suppress(Literal(';')).setResultsName('separator_token')
Comments = Optional(cppStyleComment.setResultsName('comment'))
opener, closer = Literal('{'), Literal('}')

NameDefinitions = BASE_WORDS.setResultsName('name')
ValDefinitions = OneOrMore(
    QUOTED_WORDS ^
    BASE_WORDS ^
    QuotedString('{', multiline=True, endQuoteChar='}').setParseAction(lambda t: t[0].strip())
).setResultsName('value')
VarDefinitions = Group(
    NameDefinitions + ValDefinitions
)


# NestedVar = nestedExpr(opener='{', closer='}', content=VarDefinitions)
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

Parser = OneOrMore(
        Comments +
        Expressions +
        LineSeparator
    )
