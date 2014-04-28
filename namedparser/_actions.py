# -*- coding: utf-8 -*-
from __future__ import (print_function, division, absolute_import, unicode_literals, )

from .structures import (
    Results,
    StructuresDetection,
    UnknowNode,
    DefinitionsContainer,
    ValueLists,
)


valuelists_detection = lambda s, l, t: ValueLists(t)



def expression_type_detection(st, location_of__matching_substring, toks):
    var = toks[0]
    cls = StructuresDetection.get(var['node_type'], UnknowNode)
    # if cls is None:
    #     return toks
    v = cls(var)
    return v


def expression_type_detection_in_nestedvalues(st, loc, toks):
    contents = [t for t in toks if not (isinstance(t, basestring) or t == ';')]
    return DefinitionsContainer(contents)


def result_detection(st, loc, tok):
    return Results(tok)
