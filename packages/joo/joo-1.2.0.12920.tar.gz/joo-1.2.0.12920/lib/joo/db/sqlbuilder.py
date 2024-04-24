"""
    This file is part of joo library.
    :copyright: Copyright 1993-2024 Wooloo Studio.  All rights reserved.
    :license: MIT, check LICENSE for details.
"""
def quote(v):
    return "'{}'".format(v)

def double_quote(v):
    return '"{}"'.format(v)

def backtick(v):
    return "`{}`".format(v)

def smartquote(v):
    return quote(v) if isinstance(v, str) else v    

def placeholder(v):
    return "{" + v + "}"

def parts_list(part_formatter, data_record, excludings=[]):
    parts = []
    for key, value in data_record.items():
        if key in excludings: continue
        parts.append(part_formatter(key, value))
    return parts

def parts_str(part_formatter, data_record, excludings=[], join_with=","):
    return join_with.join(parts_list(part_formatter, data_record, excludings))

"""
https://www.contrib.andrew.cmu.edu/~shadow/sql/sql1992.txt
https://jakewheat.github.io/sql-overview/sql-92-grammar.html
"""
