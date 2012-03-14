
# ------------------------------------------------------------------
# codspeechlexer.py
#
# A lexer for Codspeech
# ------------------------------------------------------------------

import sys
sys.path.insert(0,"../..")

import ply.lex as lex
from ply.lex import TOKEN

import re


# ------------------------------------------------------------------
# Tokens
# ------------------------------------------------------------------

# Reserved words
reserved = {
    # Module stuff
    'import'    : 'IMPORT',

    # Component, Controller, Network, Atom
    'Component'  : 'COMPONENT',
    'Controller' : 'CONTROLLER',
    'Network'    : 'NETWORK',
    'Atom'       : 'ATOM',
    'in'         : 'IN',
    'out'        : 'OUT',
    'default'    : 'DEFAULT',

    # Types
    'File'      : 'FILE',
    'Float'     : 'FLOAT',
    'Int'       : 'INT',
    'newtype'   : 'NEWTYPE'
    }

tokens = [
    # Literals: identifier, integer constant, float constant, string
    # constant
    'ID', 'TYPE', 'ICONST', 'FCONST', 'SCONST', 'DOCSTRING',

    # Operators: + - * / %
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MOD',

    # Assignments: =
    'EQUALS',

    # Substitution: :=
    'SUBSTITUTION',

    # Connection: <-
    'CONNECTION',

    # Delimeters: ( ) [ ] { } , . ; : ::
    'LPAREN', 'RPAREN',
    'LBRACKET', 'RBRACKET',
    'LBRACE', 'RBRACE',
    'COMMA', 'PERIOD', 'SEMI', 'COLON', 'DOUBLECOLON',

    # Other:
    'COMMENT', 'CR', 'MODULE'
    ] + reserved.values()


# ------------------------------------------------------------------
# Regular Expressions
# ------------------------------------------------------------------

digits      = r'([0-9])'
lowercase   = r'([a-z])'
uppercase   = r'([A-Z])'
letters     = r'([A-Za-z])'
nondigit    = r'([_A-Za-z])'
string      = r'([^\\\n]|(\\.))*?'
ident       = r'(' + lowercase + r'(' + digits + r'|' + nondigit + r')*)'
typeident   = r'(' + uppercase + r'(' + digits + r'|' + nondigit + r')*)'
litint      = r'\d+'
litfloat    = r'((\d+)(\.\d+)(e(\+|-)?(\d+))?)'
litstring   = r'\"' + string + r'\"'
description = r'(\{-)' + string + r'(-\})'
modulename  = r'(' + nondigit + r'(.' + nondigit + r')*' +  r')'
atommodule  = r'<( )*(?P<opt>' + modulename + r'+)( )*>'
docstring   = r'(\'\'\')(.|\n)*?(\'\'\')'


# ------------------------------------------------------------------
# default tokenizer
# ------------------------------------------------------------------

# Ignored characters
t_ignore = ' \t\x0c'

# Literals
@TOKEN(ident)
def t_ID(t):
    t.type = reserved.get(t.value,"ID")
    return t

@TOKEN(typeident)
def t_TYPE(t):
    t.type = reserved.get(t.value,"TYPE")
    return t

@TOKEN(litfloat)
def t_FCONST(t):
    t.value = float(t.value)
    return t

@TOKEN(litint)
def t_ICONST(t):
    t.value = int(t.value)
    return t

@TOKEN(litstring)
def t_SCONST(t):
    return t

# Modulename
@TOKEN(modulename)
def t_MODULE(t):
    return t

# Assignment operators
t_EQUALS       = r'='

# Substitution
t_SUBSTITUTION = r':='

# Connection
t_CONNECTION   = r'<-'

# Delimeters
t_LPAREN       = r'\('
t_RPAREN       = r'\)'
t_LBRACKET     = r'\['
t_RBRACKET     = r'\]'
t_LBRACE       = r'\{'
t_RBRACE       = r'\}'
t_COMMA        = r','
t_PERIOD       = r'\.'
t_SEMI         = r';'
t_COLON        = r':'
t_DOUBLECOLON  = r'::'


#  Other
# option for atom env. <option>
@TOKEN(atommodule)
def t_atommodule(t):
    t.type = 'MODULE'
    t.value = re.search(atommodule, t.value).group('opt')
    return t

# multline comments (/# comment #/)
def t_comment(t):
    r'/\#(.|\n)*?\#/'
    t.type = 'COMMENT'
    t.lexer.lineno += t.value.count('\n')
    pass

# single line comment (# comment)
def t_comment2(t):
    r'\#[^\\\n]*'
    t.type = 'COMMENT'
    pass

def t_CR(t):
    r'\n'
    t.lexer.lineno += len(t.value)
    return t

@TOKEN(docstring)
def t_docstring(t):
    t.type = 'DOCSTRING'
    t.lexer.lineno += t.value.count('\n')
    #doc = re.search(docstring, t.value).group('doc')
    t.value = re.sub(r'\n( )*','\n',t.value)
    t.value = re.sub(r'(\'\'\')','',t.value)
    return t


def t_error(t):
    print "Illegal character %s" % repr(t.value[0])
    t.lexer.skip(1)


# ------------------------------------------------------------------
# create lexer
# ------------------------------------------------------------------
lexer = lex.lex()




# ------------------------------------------------------------------
# useful functions
# ------------------------------------------------------------------




# ------------------------------------------------------------------
# some tests
# ------------------------------------------------------------------

example2 = '../examples/example2.cod'
example3 = '../examples/example3.cod'

def test(path):
    f = open(path)
    s = f.read()

    lex.lex()
    lexer.lineno = 1
    lex.input(s)
    while 1:
        tok = lex.token()
        if not tok: break
        print tok

