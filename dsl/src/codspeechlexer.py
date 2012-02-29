
# ------------------------------------------------------------------
# codspeechlexer.py
#
# A lexer for Codspeech
# ------------------------------------------------------------------

import sys
sys.path.insert(0,"../..")

import ply.lex as lex
from ply.lex import TOKEN

# Reserved words
reserved = {
    # Componet
    'Component' : 'COMPONENT',
    'in'        : 'IN',
    'out'       : 'OUT',
    'default'   : 'DEFAULT',

    # Function

    # Network

    # Types
    'File'      : 'FILE',
    'Float'     : 'FLOAT',
    'Int'       : 'INT'
    }

tokens = [
    # Literals: identifier, integer constant, float constant, string
    # constant
    'ID', 'TYPE', 'ICONST', 'FCONST', 'SCONST', 'DESCRIPTION',

    # Operators:

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
    ] + reserved.values()

# Complex REs
digit     = r'([0-9])'
lowercase = r'([a-z])'
uppercase = r'([A-Z])'
nondigit  = r'([_A-Za-z])'
string    = r'([^\\\n]|(\\.))*?'
ident     = r'(' + lowercase + r'(' + digit + r'|' + nondigit + r')*)'
typeident = r'(' + uppercase + r'(' + digit + r'|' + nondigit + r')*)'
litint    = r'\d+'
litfloat  = r'((\d+)(\.\d+)(e(\+|-)?(\d+))?)'
litstring = r'\"' + string + r'\"'
description = r'(\{-)' + string + r'(-\})'

# Ignored characters
t_ignore = ' \t\x0c'

# Literals
@TOKEN(ident)
def t_ID(t):
    t.type = reserved.get(t.value,"ID")
    return t

@TOKEN(typeident)
def t_TYPEID(t):
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

@TOKEN(description)
def t_DESCRIPTION(t):
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

def t_newline(t):
    r'\n'
    t.lexer.lineno += len(t.value)

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
