
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

# Lexer states
states = (('doc','exclusive'),)



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
    'ATOMOPTION'
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
atomoption  = r'<(?P<opt>' + letters + r'+)>'


# ------------------------------------------------------------------
# Token rules
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

# Other
@TOKEN(atomoption)
def t_ATOMOPTION(t):
    t.type = 'ATOMOPTION'
    m = re.search(atomoption, t.value)
    t.value = m.group('opt')
    return t

def t_newline(t):
    r'\n'
    t.lexer.lineno += len(t.value)

def t_start_doc(t):
    r'\'\'\''
    t.lexer.docstart = t.lexpos
    t.lexer.push_state('doc')

def t_doc_contents(t):
    r'[^\\\']+(?=\'\'\')'

def t_doc_end(t):
    r'\'\'\''
    t.type = 'DOCSTRING'
    doc = t.lexer.lexdata[t.lexer.docstart+3:t.lexpos]
    t.value = re.sub(r'\n( )*', '\n', doc)
    t.lexer.pop_state()
    t.lexer.lineno += t.value.count('\n')
    return t

t_doc_ignore = ' '

def t_doc_error(t):
    raise RuntimeError

def t_error(t):
    print "Illegal character %s" % repr(t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()




# ------------------------------------------------------------------
# some tests
# ------------------------------------------------------------------

def test(s):
    lex.lex()
    lex.input(s)
    while 1:
        tok = lex.token()
        if not tok: break
        print tok.type
        print tok.value
        print tok.lexer.lineno

