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
import re

from ansible_collections.datadope.discovery.plugins.module_utils.file_parser import lex

try:
    from ansible.module_utils import six
except:
    import six


class HashCommentsLexer(object):
    tokens = (
        'HASHCOMMENT',
    )

    states = ()

    def t_HASHCOMMENT(self,t):
        r'(?<!\\)\#(?:(?:\\\n)|[^\n\r])*'
        # Matches unescaped pound-sign, then escaped newlines or characters
        if False or not self.options.get('multilinehashcomments'):
            # If multiline hash-comments aren't allowed, ignore escaped
            # newlines
            if '\n' in t.value:
                first, second = t.value.split('\n', 1)
                t.lexer.lexpos = t.lexer.lexpos - len(second) - 1
                t.value = first
        #return t

class BaseNginxConfigLexer(object):

    # List of token names
    tokens = (
        'LBRACE',
        'RBRACE',
        'NEWLINE',
        'WHITESPACE',
        'KEYVALUE',
        'CONTEXT',
        'INCLUDE',  # nginx include command
    )


    states = (
        ('multiline', 'exclusive'),
    )

    def __init__(self, tempdir=None, debug=False):
        self._tempdir = tempdir
        self._debug = debug
        self.engine = None
        self.reset()

    def reset(self):
        self.engine = lex.lex(
            module=self,
            reflags=re.DOTALL | re.IGNORECASE,
            outputdir=self._tempdir,
            debuglog=log if self._debug else None,
            errorlog=log if self._debug else None
#            debuglog=lex.PlyLogger(sys.stdout),
#            errorlog=lex.PlyLogger(sys.stdout),
        )

    def tokenize(self, text):
        self.engine.input(text)

        tokens = []

        while True:
            token = self.engine.token()
            if not token:
                break
            tokens.append(token.value)

        return tokens

    # Tokenizer rules

    def t_LBRACE(self, t):
        r'\{'
        return t

    def t_RBRACE(self, t):
        r'\}'
        return t

    def t_INCLUDE(self, t):
        r'include[\t ]+[^\n\r]+'
        include, whitespace, value = re.split(r'([ \t]+)', t.value, maxsplit=1)
        t.value = include, re.sub(r'\s+',' ',whitespace), value.split(';')[0]
        return t

    def t_CONTEXT(self, t):
        #r'(?=([\w\.\/=\ -_]*[ \t=]+)*\{)([\w\.\/=\ -_]*)*'
        r'(?=([\w\.\/=\ -_\t~^]*)\{)([\w\.\/=\ -_\t~^]*)'
        lineno = len(re.findall(r'\r\n|\n|\r', t.value))
        return self._parse_key_value(t)


    def t_KEYVALUE(self, t):
        r'[^ \n\r\t=\#]+([ \t=]+(?:\\\#|[^\t\r\n\#}])+)*'
        lineno = len(re.findall(r'\r\n|\n|\r', t.value))
        if not ";" in t.value:
            t.lexer.code_start = t.lexer.lexpos - len(t.value)
            #t.lexer.keyvalue_level = 1
            t.lexer.begin('multiline')
        else:
            return self._parse_key_value(t)

    def t_multiline_NEWLINE(self, t):
        r'[ \t]*((\r\n|\n|\r|\\)[\t ]*)+'

    def t_multiline_WHITESPACE(self, t):
        r'[ \t]+'

    def t_multiline_close(self, t):
        #r'[^ \n\r\t=\#].*;'
        r'[^ \n\r\t\#]+((?:;])+)*'
        if ";" in t.value:
            #t.lexer.keyvalue_level -= 1
        #if t.lexer.keyvalue_level == 0:
            t.value = t.lexer.lexdata[t.lexer.code_start:
                                      t.lexer.lexpos]
            t.type = "KEYVALUE"
            t.lexer.lineno += t.value.count('\n')
            t.lexer.begin('INITIAL')
            return t

    def t_multiline_error(self, t):
        t.lexer.skip(1)
        raise Exception("Multiline illegal character '%s' on line %d" % (t.value[0], t.lineno))

    def t_NEWLINE(self, t):
        r'[ \t]*((\r\n|\n|\r|\\)[\t ]*)+'
        if t.value != '\\':
            t.lexer.lineno += 1
        return t

    def t_WHITESPACE(self, t):
        r'[ \t]+'
        return t

    def t_error(self, t):
        t.lexer.skip(1)
        raise Exception("Illegal character '%s' on line %d" % (t.value[0], t.lineno))

    @staticmethod
    def _parse_key_value(token):
            lineno = len(re.findall(r'\r\n|\n|\r', token.value))
            token.lexer.lineno += lineno
            # Grabs the first token before the first non-quoted whitespace.
            match = re.search(r'[^=\s"\']+|"([^"]*)"|\'([^\']*)\'', token.value)
            if not match:
                raise Exception(
                    'Syntax error in option-value pair %s on line '
                    '%d' % (token, lineno))
            option = match.group(0)
            if len(token.value.strip()) == len(option):
                token.value = token.value.strip(";").strip(), None, None
                return token
            # If there's more, split it out into whitespace and value.
            _, middle, value = re.split(r'((?:\s|=|\\\s)+)',
                                        token.value[len(option):], maxsplit=1)
            if not option:
                raise Exception(
                    'Syntax error in option-value pair %s on line '
                    '%d' % (token, lineno))

            # TODO: This cleanups should be on parse side
            token.value = option.strip(), re.sub(r'\s+',' ',middle), value.strip(";").strip()

            return token

def make_lexer(**options):
    lexer_class = BaseNginxConfigLexer

    lexer_class = type(str('NginxConfigLexer'),
                       (lexer_class, HashCommentsLexer),
                       {'tokens': lexer_class.tokens +
                        HashCommentsLexer.tokens,
                        'states': lexer_class.states +
                        HashCommentsLexer.states,
                        'options': options})

    return lexer_class
