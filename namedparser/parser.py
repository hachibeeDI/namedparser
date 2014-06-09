# -*- coding: utf-8 -*-
from __future__ import (division, absolute_import, )

from pyparsing import (
    Optional,
    Word,
    Literal,
    Keyword,
    OneOrMore,
    Group,
    WordEnd,
    Forward,
    White,
    ParserElement,
    CharsNotIn,
    QuotedString,
    quotedString,
    delimitedList,
    removeQuotes,
)
from pyparsing import (nums, alphanums, cppStyleComment, )
# from pyparsing import (ParseResults, )
# from pyparsing import (ParseException, )

from ._actions import (
    valuelists_detection,
    quoted_valuelists_detection,
    expression_type_detection,
    expression_type_detection_in_nestedvalues,
)


BASE_STRINGS = alphanums + "-" + "_"
NETWORK_STRINGS = alphanums + "-" + "_" + '.'  # 適時調整
BASE_WORDS = Word(BASE_STRINGS)
QUOTED_WORDS = quotedString.addParseAction(removeQuotes)
END_OF_WORDS = WordEnd(BASE_STRINGS)


LineSeparator = Literal(';').suppress().setResultsName('separator_token')
Comments = Optional(cppStyleComment.setResultsName('comment'))
opener, closer = Literal('{'), Literal('}')

# ex: {1.1.1.1; 2.2.2.2; ...}
WORD_LIST = (
    opener.suppress() +
    delimitedList(Word(NETWORK_STRINGS), delim=';') +
    LineSeparator +
    closer.suppress()
).setParseAction(valuelists_detection)

QUOTED_WORD_LIST = (
    opener.suppress() +
    delimitedList(QUOTED_WORDS, delim=';') +
    LineSeparator +
    closer.suppress()
).setParseAction(quoted_valuelists_detection)



NameDefinitions = BASE_WORDS.setResultsName('node_type')
ValDefinitions = OneOrMore(
    QUOTED_WORDS ^
    BASE_WORDS ^
    QuotedString('{', multiline=True, endQuoteChar='}').setParseAction(lambda t: t[0].strip())
).setResultsName('value')


VarDefinitions = Group(
    NameDefinitions + ValDefinitions
).setParseAction(expression_type_detection)


NestedVar = Forward().setParseAction(expression_type_detection_in_nestedvalues)
_NestedContent = (
    VarDefinitions +
    CharsNotIn('{' + '}' + ParserElement.DEFAULT_WHITE_CHARS).setParseAction(lambda t: t[0].strip())
)
NestedVar << (
    opener.suppress() +
    OneOrMore(NestedVar | _NestedContent) +
    closer.suppress()
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

KeyDefinitions = Group(
    Keyword('key').setResultsName('node_type') +
    QUOTED_WORDS.setResultsName('name') +
    NestedVar.copy().setResultsName('value')
).setResultsName('key-node')

AclDefinitions = Group(
    Keyword('acl').setResultsName('node_type') +
    QUOTED_WORDS.copy().setResultsName('name') +
    WORD_LIST.copy().setResultsName('value')
).setResultsName('acl-node')

# 'inet' node is in 'controls'
_InetDefinitions = Group(
    Keyword('inet').setResultsName('node_type') +
    Word(NETWORK_STRINGS).setResultsName('ipaddr') +
    Optional(
        Keyword('port') + Word(nums).setResultsName('value')
    ).setResultsName('port') +
    Group(
        Keyword('allow') + WORD_LIST.copy().setResultsName('value')
    ).setResultsName('allow-section') +
    Group(
        Keyword('keys') + QUOTED_WORD_LIST.copy().setResultsName('value')
    ).setResultsName('keys-section')
).setParseAction(expression_type_detection)

ControlsDefinitions = Group(
    Keyword('controls').setResultsName('node_type') +
    opener.suppress() +
    _InetDefinitions.setResultsName('inet-node') +
    LineSeparator +
    closer.suppress()
).setResultsName('controls-node')


Expressions = OneOrMore(
    ZoneDefinitions |
    KeyDefinitions |
    OptionsDefinitions |
    AclDefinitions |
    ControlsDefinitions |
    VarDefinitions
).setParseAction(expression_type_detection)

_Parser = OneOrMore(
    Comments +
    Expressions +
    LineSeparator
)
