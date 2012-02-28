
# ------------------------------------------------------------------
# codspeechlexer.py
#
# A lexer for Codspeech
# ------------------------------------------------------------------

import sys
sys.path.insert(0,"../..")

import ply.lex as lex

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

tokens = (
    # Literals
    # (identifier, integer constant, float constant, string constant)
    'ID', 'TYPEID', 'ICONST', 'FCONST', 'SCONST',

    # Operators
    # ()

    # Assignments
    # (=)
    'EQUALS',

    # Substitution :=
    'SUBST',

    # Connection <-
    'CONNECTION',

    # Delimeters
    # ( ) [ ] { } , . ; : ::
    'LPAREN', 'RPAREN',
    'LBRACKET', 'RBRACKET',
    'LBRACE', 'RBRACE',
    'COMMA', 'PERIOD', 'SEMI', 'COLON', 'DOUBLECOLON'
    )

# Ignored characters
t_ignore = ' \t\x0c'

# Literals


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
r_SEMI         = r';'
r_COLON        = r':'
r_DOUBLECOLON  = r'::'
