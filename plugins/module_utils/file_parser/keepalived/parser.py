#
# This file is part of apacheconfig software.
#
# Copyright (c) 2018-2020, Ilya Etingof <etingof@gmail.com>
# License: https://github.com/etingof/apacheconfig/LICENSE.rst
#
from __future__ import (absolute_import, division, print_function)

from __future__ import unicode_literals

__metaclass__ = type

import logging

from ansible_collections.datadope.discovery.plugins.module_utils.file_parser import yacc

try:
    from ansible.module_utils import six
except:
    import six


log = logging.getLogger(__name__)


class HashCommentsParser(object):
    def p_hashcomment(self, p):
        """comment : HASHCOMMENT
        """
        p[0] = ['comment', p[1]]


class BaseKeepAlivedConfigParser(object):

    def __init__(self, lexer, start='config', tempdir=None, debug=False):
        self._lexer = lexer
        self.tokens = lexer.tokens  # parser needs this implicitly
        self._tempdir = tempdir
        self._debug = debug
        self._start = start
        self._preserve_whitespace = self.options.get('preservewhitespace',
                                                     False)
        self.engine = None
        self.reset()

    def reset(self):
        self.engine = yacc.yacc(
            module=self,
            start=self._start,
            outputdir=self._tempdir,
            write_tables=bool(self._tempdir),
            debug=self._debug,
#            debuglog=yacc.PlyLogger(sys.stdout),
#            errorlog=yacc.PlyLogger(sys.stdout),
            debuglog=log if self._debug else yacc.NullLogger(),
            errorlog=log if self._debug else yacc.NullLogger(),
        )

    def parse(self, text):
        self.reset()
        return self.engine.parse(text)

    # PARSING RULES
    # =============

    def p_requirednewline(self, p):
        """requirednewline : NEWLINE
        """
        p[0] = ['newline']

    def p_whitespace(self, p):
        """whitespace : requirednewline
                      | WHITESPACE
        """
        p[0] = ['whitespace']

    def p_statement(self, p):
        """statement : KEYVALUE
        """
        p[0] = ['statement']
        if self._preserve_whitespace:
            p[0] += p[1]
        else:
            if len(p[1]) > 1:
                p[0] += [p[1][0], p[1][2]]
            else:
                p[0] += p[1]

        if self.options.get('lowercasenames'):
            p[0][1] = p[0][1].lower()


    def p_item(self, p):
        """item : statement
                | block
        """
        p[0] = p[1]

    def p_block(self, p):
        """block : CONTEXT LBRACE contents RBRACE
        """
        if p[1][1] == None:
            p[1] = [p[1][0]]

        p[0] = ['block', p[1], p[3]]

        if self.options.get('lowercasenames'):
            p[0][1] = tuple(x.lower() for x in p[0][1])
            p[0][3] = p[0][3].lower()


    def p_startitem(self, p):
        """startitem : whitespace item
                     | item
                     | comment
        """
        if len(p) == 3:
            if self._preserve_whitespace:
                item = p[2]
                p[0] = [item[0]] + [p[1]] + item[1:]
            else:
                p[0] = p[2]
        else:
            p[0] = p[1]

    def p_miditem(self, p):
        """miditem : requirednewline item
                   | whitespace comment
                   | comment
        """
        if len(p) == 3:
            if self._preserve_whitespace:
                item = p[2]
                p[0] = [item[0]] + [p[1]] + item[1:]
            else:
                p[0] = p[2]
        else:
            p[0] = p[1]

    def p_contents(self, p):
        """contents : contents whitespace
                    | contents miditem
                    | whitespace
                    | startitem
        """
        n = len(p)
        if n == 3:
            if isinstance(p[2], six.text_type) and p[2].isspace():
                # contents whitespace
                if self._preserve_whitespace:
                    p[0] = p[1] + [p[2]]
                else:
                    p[0] = p[1]
            else:
                # contents miditem
                p[0] = p[1] + [p[2]]
        else:
            if (not self._preserve_whitespace and
               isinstance(p[1], six.text_type) and p[1].isspace()):
                # whitespace
                # (if contents only consists of whitespace)
                p[0] = []
            else:
                # startitem
                p[0] = ['contents', p[1]]

    def p_config(self, p):
        """config : config contents
                  | contents
        """
        n = len(p)
        if n == 3:
            p[0] = p[1] + [p[2]]
        elif n == 2:
            p[0] = ['config', p[1]]



    def p_error(self, p):
        raise Exception("Parser error at '{}'".format(p.value)
                                if p else 'Unexpected EOF')


def make_parser(**options):

    parser_class = BaseKeepAlivedConfigParser

    parser_class = type(str('KeepAlivedConfigParser'),
                        (parser_class, HashCommentsParser),
                        {'options': options})

    return parser_class
